// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import { cleanup } from "@testing-library/vue";
import { afterEach, describe, expect, it, vi } from "vitest";
import DestinationTag from "./DestinationTag.vue";
import { render } from "./test-utils";
import type { Destination } from "@/api/types";

vi.mock("../auth");

describe("DestinationTag", () => {
  afterEach(() => {
    cleanup();
  });

  it("check we show the text when icononly is false", () => {
    const dest: Destination = {
      protocol: "irc",
      address: "freednode.net",
    };
    const props = { destination: dest, icononly: false };
    const { getByText } = render(DestinationTag, props);
    expect(getByText("freednode.net")).toBeInTheDocument();
    expect(getByText("irc:")).toBeInTheDocument();
  });
  it("check we show the text when icononly is true", () => {
    const dest: Destination = {
      protocol: "irc",
      address: "freednode.net",
    };
    const props = { destination: dest, icononly: true };
    const { queryByText } = render(DestinationTag, props);
    expect(queryByText("freednode.net")).toBeNull();
    expect(queryByText("irc:")).toBeNull();
  });
});
