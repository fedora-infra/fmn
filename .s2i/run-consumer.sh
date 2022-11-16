#!/bin/bash

set -e

# We install the app in a specific virtualenv:
export PATH=/opt/app-root/src/.local/venvs/fmn/bin:$PATH

# Run the application
fedora-messaging --conf /etc/fmn/consumer.toml consume --callback fmn.consumer:Consumer
