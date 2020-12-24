#!/bin/python3
"""
Buildozer action
================

It sets some environment variables, installs Buildozer, runs Buildozer and finds
output file.

You can read this file top down because functions are ordered by their execution
order.
"""

import os
import subprocess
import sys
from os import environ as env


def main():
    repository_root = os.path.abspath(env["INPUT_REPOSITORY_ROOT"])
    change_owner(env["USER"], repository_root)
    fix_home()
    install_buildozer(env["INPUT_BUILDOZER_VERSION"])
    apply_buildozer_settings()
    change_directory(env["INPUT_REPOSITORY_ROOT"], env["INPUT_WORKDIR"])
    apply_patches()
    run_command(env["INPUT_COMMAND"])
    set_output(env["INPUT_REPOSITORY_ROOT"], env["INPUT_WORKDIR"])
    change_owner("root", repository_root)


def change_owner(user, repository_root):
    # GitHub sets root as owner of repository directory. Change it to user
    # And return to root after all commands
    subprocess.check_call(["sudo", "chown", "-R", user, repository_root])


def fix_home():
    # GitHub sets HOME to /github/home, but Buildozer is installed to /home/user. Change HOME to user's home
    env["HOME"] = env["HOME_DIR"]


def install_buildozer(buildozer_version):
    # Install required Buildozer version
    print("::group::Installing Buildozer")
    pip_install = [sys.executable] + "-m pip install --user --upgrade".split()
    if buildozer_version == "stable":
        # Install stable buildozer from PyPI
        subprocess.check_call([*pip_install, "buildozer"])
    elif os.path.exists(buildozer_version) and os.path.exists(
        os.path.join(buildozer_version, "buildozer", "__init__.py")
    ):
        # Install from local directory
        subprocess.check_call([*pip_install, buildozer_version])
    elif buildozer_version.startswith("git+"):
        # Install from specified git+ link
        subprocess.check_call([*pip_install, buildozer_version])
    elif buildozer_version == "":
        # Just do nothing
        print(
            "::warning::Buildozer is not installed because "
            "specified buildozer_version is nothing."
        )
    else:
        # Install specified ref from repository
        subprocess.check_call(
            [
                *pip_install,
                f"git+https://github.com/kivy/buildozer.git@{buildozer_version}",
            ]
        )
    print("::endgroup::")


def apply_buildozer_settings():
    # Buildozer settings to disable interactions
    env["BUILDOZER_WARN_ON_ROOT"] = "0"
    env["APP_ANDROID_ACCEPT_SDK_LICENSE"] = "1"
    # Do not allow to change directories
    env["BUILDOZER_BUILD_DIR"] = "./.buildozer"
    env["BUILDOZER_BIN"] = "./bin"


def change_directory(repository_root, workdir):
    directory = os.path.join(repository_root, workdir)
    # Change directory to workir
    if not os.path.exists(directory):
        print("::error::Specified workdir is not exists.")
        exit(1)
    os.chdir(directory)


def apply_patches():
    # Apply patches
    print("::group::Applying patches to Buildozer")
    try:
        import importlib
        import site

        importlib.reload(site)
        globals()["buildozer"] = importlib.import_module("buildozer")
    except ImportError:
        print(
            "::error::Cannot apply patches to buildozer (ImportError). "
            "Update buildozer-action to new version or create a Bug Request"
        )
        print("::endgroup::")
        return

    print("Changing global_buildozer_dir")
    source = open(buildozer.__file__, "r", encoding="utf-8").read()
    new_source = source.replace(
        """
    @property
    def global_buildozer_dir(self):
        return join(expanduser('~'), '.buildozer')
""",
        f"""
    @property
    def global_buildozer_dir(self):
        return '{env["GITHUB_WORKSPACE"]}/{env["INPUT_REPOSITORY_ROOT"]}/.buildozer_global'
""",
    )
    if new_source == source:
        print(
            "::warning::Cannot change global buildozer directory. "
            "Update buildozer-action to new version or create a Bug Request"
        )
    open(buildozer.__file__, "w", encoding="utf-8").write(new_source)
    print("::endgroup::")


def run_command(command):
    # Run command
    retcode = subprocess.check_call(command, shell=True)
    if retcode:
        print(f'::error::Error while executing command "{command}"')
        exit(1)


def set_output(repository_root, workdir):
    if not os.path.exists("bin"):
        print(
            "::error::Output directory does not exist. See Buildozer log for error"
        )
        exit(1)
    filename = [
        file
        for file in os.listdir("bin")
        if os.path.isfile(os.path.join("bin", file))
    ][0]
    path = os.path.normpath(
        os.path.join(repository_root, workdir, "bin", filename)
    )
    print(f"::set-output name=filename::{path}")


if __name__ == "__main__":
    main()
