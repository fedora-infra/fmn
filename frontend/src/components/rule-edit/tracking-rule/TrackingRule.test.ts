// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { vueQueryPluginOptions } from "@/api";
import { TRACKING_RULES } from "@/api/constants";
import { config as formkitConfig } from "@/forms/index";
import { useUserStore } from "@/stores/user";
import { plugin as FormKitPlugin } from "@formkit/vue";
import { VueQueryPlugin } from "@tanstack/vue-query";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  type RenderOptions,
} from "@testing-library/vue";
import { createPinia, setActivePinia } from "pinia";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { defineComponent } from "vue";
import TrackingRule from "./TrackingRule.vue";

const renderOptions: RenderOptions = {
  global: {
    plugins: [
      [FormKitPlugin, formkitConfig],
      [VueQueryPlugin, vueQueryPluginOptions],
    ],
  },
};

const chooseOption = async (comboboxNumber: number, label: string) => {
  // Open the select
  const combobox = screen.getAllByRole("combobox")[comboboxNumber];
  combobox.focus();
  await fireEvent.mouseDown(combobox);
  await waitFor(() =>
    expect(combobox).toHaveAttribute("aria-expanded", "true"),
  );
  // Choose an option
  await fireEvent.mouseDown(screen.getByText(label));
};

describe("TrackingRule", () => {
  beforeEach(async () => {
    setActivePinia(createPinia());
    // Make sure we have a user logged in
    const store = useUserStore();
    store.$patch({
      accessToken: "testing",
      username: "dummy-user",
      fullName: "Dummy User",
      email: "dummy@example.com",
    });
  });
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  const Component = defineComponent({
    props: ["submitHandler", "initialValue"],
    components: { TrackingRule },
    template: `
      <FormKit type="form" @submit="submitHandler" :value="initialValue">
          <TrackingRule />
      </FormKit>`,
  });

  it("renders", async () => {
    const { getAllByRole } = render(Component, renderOptions);
    const listElements = getAllByRole("option");

    expect(await getAllByRole("option")).toHaveLength(TRACKING_RULES.length);
    TRACKING_RULES.forEach((tr, index) => {
      expect(listElements[index]).toHaveTextContent(tr.label);
      expect(listElements[index]).toHaveTextContent(tr.description);
    });
  });

  it("displays default param values", async () => {
    const { getAllByText, findAllByRole } = render(Component, {
      props: {
        initialValue: {
          tracking_rule: {
            name: TRACKING_RULES[2].name,
            params: [{ type: "dummy", name: "artifact" }],
          },
        },
      },
      ...renderOptions,
    });

    const options = await findAllByRole("option");
    expect(options[2]).toHaveAttribute("aria-selected", "true");
    expect(options[2]).toHaveAttribute("data-selected", "true");
    expect(options[2]).toHaveAttribute(
      "class",
      "multiselect-option is-selected",
    );
    await waitFor(() => {
      const results = getAllByText("dummy/artifact");
      expect(results[0].parentNode).toHaveClass("multiselect-tag");
    });
  });

  it("sets a default param value for artifact-owned", async () => {
    const { getAllByText } = render(Component, renderOptions);

    await chooseOption(0, TRACKING_RULES[0].label);

    await waitFor(() => {
      const results = getAllByText("dummy-user");
      expect(results[0].parentNode).toHaveClass("multiselect-tag");
    });
  });

  it("sets a default param value for artifact-owned when another rule was selected", async () => {
    const { getAllByText } = render(Component, {
      props: {
        initialValue: {
          tracking_rule: {
            name: TRACKING_RULES[2].name,
            params: [{ type: "dummy", name: "artifact" }],
          },
        },
      },
      ...renderOptions,
    });

    await chooseOption(0, TRACKING_RULES[0].label);

    await waitFor(() => {
      const results = getAllByText("dummy-user");
      expect(results[0].parentNode).toHaveClass("multiselect-tag");
    });
  });

  it("resets the param value when another rule is selected", async () => {
    const { queryAllByText } = render(Component, {
      props: {
        initialValue: {
          tracking_rule: {
            name: TRACKING_RULES[2].name,
            params: [{ type: "dummy", name: "artifact" }],
          },
        },
      },
      ...renderOptions,
    });
    // Wait until it's all rendered
    await waitFor(() => {
      screen.getAllByText("dummy/artifact");
    });
    // Select another tracking rule
    await chooseOption(0, TRACKING_RULES[4].label);
    await waitFor(async () => {
      // Previous values should have been removed
      expect(queryAllByText("dummy/artifact")).toHaveLength(0);
      // The params box should be empty
      const comboboxes = screen.getAllByRole("combobox");
      const parentBox = comboboxes[1].parentNode?.parentNode;
      expect(parentBox).toHaveClass("multiselect-tags");
      expect(parentBox).toHaveTextContent(/^$/);
    });
  });
});
