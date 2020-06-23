#!/bin/bash

# GitHub sets root as owner of repository directory. Change it to user
sudo chown -R "$USER" "$GITHUB_WORKSPACE"
# GitHub sets HOME to /github/home, but Buildozer is installed to /home/user. Change HOME to user's home
export HOME=$HOME_DIR

# Install required Buildozer version
echo ::group::Installing Buildozer
PIP_INSTALL="pip3 install --user --upgrade"
if [[ "$INPUT_BUILDOZER_VERSION" == "stable" ]]; then
  $PIP_INSTALL buildozer  # Install stable buildozer from PyPI
elif [[ -d "$INPUT_BUILDOZER_VERSION" ]]; then
  $PIP_INSTALL "$INPUT_BUILDOZER_VERSION"  # Install from local directory
elif [[ "$INPUT_BUILDOZER_VERSION" == "git+"* ]]; then
  $PIP_INSTALL "$INPUT_BUILDOZER_VERSION"  # Install from specified git+ link
elif [[ "$INPUT_BUILDOZER_VERSION" == "" ]]; then
  echo ::warning::Buildozer is not installed because specified buildozer_version is nothing.  # Just do nothing
else
  $PIP_INSTALL "git+https://github.com/kivy/buildozer.git@$INPUT_BUILDOZER_VERSION"  # Install specified ref from repository
fi
echo ::endgroup::

# Buildozer settings to disable interactions
export BUILDOZER_WARN_ON_ROOT=0
export APP_ANDROID_ACCEPT_SDK_LICENSE=1
# Do not allow to change directories
export BUILDOZER_BUILD_DIR=./.buildozer
export BUILDOZER_BIN=./bin

# Change directory to workir
if ! cd "$INPUT_WORKDIR"; then
  echo ::error::Specified workdir is not exists.
  exit 1
fi

# Run command
if ! sh -c "$INPUT_COMMAND"; then
  echo ::error::Error while executing command \""$INPUT_COMMAND"\"
  exit 1
fi

# Give access to root
sudo chown -R root "$GITHUB_WORKSPACE"

# Set output
if [ ! -d bin ]; then
  echo ::error::Output directory does not exist. See Buildozer log for error
  exit 1
fi
filename=$(ls bin | head -n1)
echo ::set-output name=filename::"$INPUT_WORKDIR/bin/$filename"
