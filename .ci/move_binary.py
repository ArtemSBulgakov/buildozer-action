#!/bin/python3
import os
import shutil
import subprocess
import sys
from os import environ as env

binary_filename = os.path.abspath(sys.argv[1])
master_repository_directory = os.path.abspath(sys.argv[2])
data_repository = sys.argv[3]
data_repository_directory = os.path.abspath(data_repository)
directory = sys.argv[4]

os.chdir(master_repository_directory)

filename = os.path.basename(binary_filename)
# Include commit subject and hash to the new commit 
commit_hash = (
    subprocess.check_output(["git", "rev-parse", "--verify", "--short", "HEAD"])
    .decode("utf-8")
    .strip()
)
commit_subject = (
    subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"])
    .decode("utf-8")
    .strip()
)

is_tag = env["GITHUB_EVENT_NAME"] == "push" and env["GITHUB_REF"].startswith(
    "refs/tags"
)
is_pr = env["GITHUB_REF"].startswith("refs/pull")

filename_split = filename.split("-")
if is_tag:
    new_commit_message = (
        f'Add binary for {filename_split[1]} {commit_hash}: "{commit_subject}"'
    )
elif is_pr:
    # Pull Request - prN (pr1)
    pr_number = env["GITHUB_REF"].split("/")[2]
    filename = "-".join(
        [*filename_split[:2], f"pr{pr_number}", *filename_split[2:]]
    )
    directory = os.path.join(directory, "prs")
    new_commit_message = (
        f'Add binary for #{pr_number} {commit_hash}: "{commit_subject}"'
    )
else:
    # Latest commit - short hash (20f2448)
    filename = "-".join([*filename_split[:2], commit_hash, *filename_split[2:]])
    new_commit_message = f'Add binary for {commit_hash}: "{commit_subject}"'

# Set author info to the latest commit author
author_name = subprocess.check_output(
    ["git", "log", "-1", "--pretty=format:%an"]
).decode("utf-8")
author_email = subprocess.check_output(
    ["git", "log", "-1", "--pretty=format:%ae"]
).decode("utf-8")

# Prepare for pushing
os.chdir(data_repository_directory)
os.makedirs(directory, exist_ok=True)
subprocess.check_call(["git", "config", "user.name", author_name])
subprocess.check_call(["git", "config", "user.email", author_email])
# Ensure that there are no changes
subprocess.check_call(
    [
        "git",
        "pull",
        "origin",
        data_repository,
        "--ff-only",
        "--allow-unrelated-histories",
    ]
)

# Try to push several times
for i in range(3):
    shutil.copy(binary_filename, os.path.join(directory, filename))
    # Push changes
    subprocess.check_call(["git", "add", os.path.join(directory, filename)])
    subprocess.check_call(
        ["git", "commit", "--amend", "-m", new_commit_message]
    )
    try:
        subprocess.check_call(
            ["git", "push", "origin", data_repository, "--force"]
        )
    except subprocess.CalledProcessError:  # There are changes in repository
        # Undo local changes
        subprocess.check_call(
            ["git", "reset", f"origin/{data_repository}", "--hard"]
        )
        # Pull new changes
        subprocess.check_call(
            [
                "git",
                "pull",
                "origin",
                data_repository,
                "--force",
                "--ff-only",
                "--allow-unrelated-histories",
            ]
        )
    else:
        break  # Exit loop if there is no errors
else:
    raise Exception("Cannot push binary")

new_commit_hash = (
    subprocess.check_output(["git", "rev-parse", "--verify", "--short", "HEAD"])
    .decode("utf-8")
    .strip()
)
print(
    f"Binary file: {env['GITHUB_SERVER_URL']}/{env['GITHUB_REPOSITORY']}/blob/"
    f"{new_commit_hash}/{directory}/{filename}"
)
