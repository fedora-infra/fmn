#!/bin/bash

# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

set -e

# We install the app in a specific virtualenv:
export PATH=/opt/app-root/src/.local/venvs/fmn/bin:$PATH

# Run the application
exec fmn-sender --config /etc/fmn/sender-email.toml
