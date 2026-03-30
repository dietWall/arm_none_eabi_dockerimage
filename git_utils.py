#! /usr/bin/env python3

import subprocess


def get_repo_root() -> str:
    import subprocess    
    git_result = subprocess.run(["git", "rev-parse", "--show-toplevel"],capture_output=True)
    repo_root = git_result.stdout.strip().decode("utf-8")
    return repo_root

def get_branch_name() -> str:
    import subprocess    
    git_result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],capture_output=True)
    branch_name = git_result.stdout.strip().decode("utf-8")
    return branch_name

def create_git_tag(version: str) -> subprocess.CompletedProcess:
    import subprocess
    tag_name = f"{version}"
    return subprocess.run(["git", "tag", tag_name], check=True)

def get_git_tag() -> str:
    import subprocess
    git_result = subprocess.run(["git", "describe", "--tags"], capture_output=True)
    tag_name = git_result.stdout.strip().decode("utf-8")
    print(f"Current git tag: {tag_name}")
    return tag_name

if __name__ == "__main__":
    print(get_repo_root())
    print(get_branch_name())