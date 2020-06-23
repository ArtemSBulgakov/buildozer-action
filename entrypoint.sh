#!/bin/bash

# GitHub sets root as owner of repository directory. Change it to user
sudo chown -R "$USER" "$GITHUB_WORKSPACE"
# GitHub sets HOME to /github/home, but Buildozer is installed to /home/user. Change HOME to user's home
export HOME=$HOME_DIR

# Run build
sh -c "buildozer android debug"

# Give access to root
sudo chown -R root "$GITHUB_WORKSPACE"
