#!/bin/sh

set -e
# set -x

export DEBIAN_FRONTEND=noninteractive

# Install dependencies
apt-get update -y -qq
apt-get install -y -qq \
  bash \
  curl \
  jq \
  git \
  unzip \
  time \
  gettext \
  ca-certificates \
  gnupg \
  lsb-release \
  python3-pip \
  libpq-dev

time rm -rf /var/lib/apt/lists/*
