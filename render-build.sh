#!/usr/bin/env bash

# Install Chrome dependencies
apt-get update && apt-get install -y wget gnupg2 ca-certificates

# Download and install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb || apt-get install -f -y

# Clean up Chrome installation files
rm -f google-chrome-stable_current_amd64.deb
