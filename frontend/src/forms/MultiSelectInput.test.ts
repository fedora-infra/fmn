// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import type { FormKitGroupValue } from "@formkit/core";
import { plugin as FormKitPlugin } from "@formkit/vue";
import {
  cleanup,
  fireEvent,
  render,
  waitFor,
  type RenderOptions,
} from "@testing-library/vue";
import { afterEach, describe, expect, it } from "vitest";
import { defineComponent } from "vue";
import { config as formkitConfig } from "./index";

const renderOptions: RenderOptions = {
  global: {
    plugins: [[FormKitPlugin, formkitConfig]],
  },
};

describe("MultiSelectInput", () => {
  afterEach(() => {
    cleanup();
  });

  it("is properly connected to FormKit", async () => {
    const Component = defineComponent({
      props: ["handler"],
      template: `
              <FormKit type="form" @submit="handler">
              <FormKit
              type="multiselect"
              name="component"
              placeholder="Placeholder"
              :msOptions="['a', 'b', 'c']"
            />
            </FormKit>`,
    });
    const submittedValues: FormKitGroupValue[] = [];
    const handler = (data: FormKitGroupValue) => {
      submittedValues.push(data);
    };

    const { getByText } = render(Component, {
      props: { handler },
      ...renderOptions,
    });
    const submitButton = getByText("Submit");

    await fireEvent.mouseDown(getByText("b"));
    await fireEvent.click(submitButton);
    await waitFor(() => expect(submittedValues).toHaveLength(1));
    expect(submittedValues[0]).toMatchObject({ component: "b" });
  });

  it("forwards options and labels properly", async () => {
    const Component = defineComponent({
      props: ["handler"],
      template: `
              <FormKit type="form" @submit="handler">
              <FormKit
              type="multiselect"
              name="component"
              mode="tags"
              object
              :msOptions="[{attr1: 'a1', attr2: 'b1'},{attr1: 'a2', attr2: 'b2'}]"
              msLabel="attr2"
            />
            </FormKit>`,
    });
    const submittedValues: FormKitGroupValue[] = [];
    const handler = (data: FormKitGroupValue) => {
      submittedValues.push(data);
    };

    const { getByText, findAllByRole } = render(Component, {
      props: { handler },
      ...renderOptions,
    });

    // Verify that the attr2 values have been used as option labels
    const options = await findAllByRole("option");
    expect(options).toHaveLength(2);
    expect(options[0]).toHaveTextContent("b1");
    expect(options[1]).toHaveTextContent("b2");

    // Verify that we get the entire option object on submission
    await fireEvent.mouseDown(getByText("b2"));
    await fireEvent.click(getByText("Submit"));
    await waitFor(() => expect(submittedValues).toHaveLength(1));
    expect(submittedValues[0]).toMatchObject({
      component: [{ attr1: "a2", attr2: "b2" }],
    });
  });

  it("renders a tag select properly", async () => {
    const Component = defineComponent({
      props: ["options", "handler"],
      template: `
          <FormKit type="form" @submit="handler">
          <FormKit
          type="multiselect"
          name="component"
          mode="tags"
          placeholder="Placeholder"
          :msOptions="options"
          :close-on-select="false"
          />
          </FormKit>`,
    });
    const submittedValues: FormKitGroupValue[] = [];
    const handler = (data: FormKitGroupValue) => {
      submittedValues.push(data);
    };

    const { getByText, getByRole } = render(Component, {
      props: { options: ["a", "b", "c"], handler },
      ...renderOptions,
    });

    const submitButton = getByText("Submit");
    const selectInput = getByRole("combobox");

    // Open the select
    selectInput.focus();
    await fireEvent.mouseDown(selectInput);
    await waitFor(() =>
      expect(selectInput).toHaveAttribute("aria-expanded", "true"),
    );
    // Choose an option
    await fireEvent.mouseDown(getByText("b"));
    // The select must not have closed
    expect(selectInput).toHaveAttribute("aria-expanded", "true");
    // Submit the form
    await fireEvent.click(submitButton);
    await waitFor(() => expect(submittedValues).toHaveLength(1));
    expect(submittedValues[0]).toMatchObject({ component: ["b"] });
  });
});
