#! /usr/bin/env python3

import os
import argparse
from typing import Union
from semver.version import Version
from git_utils import *

def get_version(path: Union[str, os.PathLike]) -> Version:
    """
    Construct a Version object from a file

    :param path: A text file only containing the semantic version
    :return: A :class:`Version` object containing the semantic
             version from the file.
    """
    version = open(path,"r").read().strip()
    return Version.parse(version)

def increase_version(version: Version, bump_type: str) -> Version:
    """
    Increase a version by a given bump type

    :param version: The version to increase
    :param bump_type: The type of increase, either "major", "minor" or "patch"
    :return: A new :class:`Version` object with the increased version
    """
    if bump_type == "major":
        return version.bump_major()
    elif bump_type == "minor":
        return version.bump_minor()
    elif bump_type == "patch":
        return version.bump_patch()
    else:
        return version.bump_build()

def write_version(path: Union[str, os.PathLike], version: Version) -> None:
    """
    Write a version to a file

    :param path: A text file to write the version to
    :param version: The version to write to the file
    """
    with open(path, "w") as f:
        f.write(str(version))

def create_tag(version: Version) -> None:
    """
    Create a git tag for a given version

    :param version: The version to create a tag for
    """
    result = create_git_tag(str(version))
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create git tag with return code {result.returncode}: {result.stdout}, {result.stderr}")

def main():
    parser = argparse.ArgumentParser(description="Bump version in version.txt")
    parser.add_argument("--bump_type", "-b", choices=["major", "minor", "patch", "build"], help="Type of version bump", required=True)
    parser.add_argument("--file", default="version",help="File containing the current version")
    args = parser.parse_args()

    current_version = get_version(args.file)
    new_version = increase_version(current_version, args.bump_type)
    
    #check if this is what the user wants to do
    print(f"Bumping version from {current_version} to {new_version}")
    confirm = input("Do you want to continue? (y/n): ")
    if confirm.lower() != "y":
        print("Aborting version bump.")
        return
    
    write_version(args.file, new_version)
    create_tag(new_version)


if __name__ == "__main__":
    main()