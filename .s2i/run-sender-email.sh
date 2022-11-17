#!/bin/bash

set -e

# We install the app in a specific virtualenv:
export PATH=/opt/app-root/src/.local/venvs/fmn/bin:$PATH

# Run the application
fmn-sender --config /etc/fmn/sender-irc.toml
