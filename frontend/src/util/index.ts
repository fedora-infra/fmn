// SPDX-FileCopyrightText: Contributors to the Fedora Project
//
// SPDX-License-Identifier: MIT

import md5 from "crypto-js/md5";

export function generateLibravatarURL(
  email: string | null,
  size = 80,
  defaulticon = "retro",
): string {
  const hash = md5(email || "nobody@fedoraproject.org");
  return `https://www.libravatar.org/avatar/${hash}?s=${size.toString()}&d=${defaulticon}`;
}

// https://stackoverflow.com/a/46700791
export function isDefined<T>(item: T | undefined): item is T {
  return typeof item !== "undefined";
}
