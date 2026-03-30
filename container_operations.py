#! /usr/bin/env python3

import sys

import docker
import argparse
import os
from git_utils import *

default_tag="ghcr.io/dietwall/arm_gcc_image"


def get_container(tag: str = default_tag):
    client = docker.from_env()
    containers = client.containers.list(all=True, filters={"ancestor": f"{tag}"})
    print(f"{len(containers)} of containers found with image: {tag}")
    if len(containers) == 0:
        raise Exception(f"No containers found with image: {tag}, please start one with --run")
    if len(containers) > 1:
        print(f"WARN: Multiple containers found with image: {tag}, using the first one, id: {containers[0].id}")
    return containers[0]

def run_tests(tag: str = default_tag):
    #get the container id
    id = get_container(tag=tag).id
    print(f"running tests in container: {id}")
    repo_root = get_repo_root()
    #call pytest on host with container id
    import pytest
    retcode = pytest.main(["-v", "-s", f"{repo_root}/test", f"--container_id={id}", f"--junitxml={repo_root}/test_results.xml"])
    if retcode != 0:
        raise Exception(f"Tests failed with code: {retcode}")
    print("All tests passed")

def build_image(tag: str = default_tag, 
        user: str = "developer", 
        uid: int = os.getuid(), 
        gid: int = os.getgid(),
        labels: dict[str, str]|None = None
        ):
    client = docker.from_env()
    buildsystem_dir = get_repo_root()
    print(f"building image in {buildsystem_dir}, tagging with: {tag}")
    try:
        image, build_logs = client.images.build(path=buildsystem_dir, tag=f"{tag}", buildargs={"user":user, "uid": f"{uid}", "gid":f"{gid}"}, labels=labels)
        # for streaming the logs in realtime, we need to use client.build instead of client.images.build, as of now it is good enough
        # this one buffers and prints it afterwards
        for chunk in build_logs:
            if 'stream' in chunk:
                for line in chunk['stream'].splitlines():
                    print(line)
        print(f"Built image with id: {image.id}")
    except Exception as err:
        print(f"error on build: {err}")

def get_labels() -> dict[str, str]:
    repo_root = get_repo_root()
    labels = {}
    labels["org.opencontainers.image.source"] = default_tag
    labels["org.opencontainers.image.version"] = get_git_tag() 
    labels["org.opencontainers.image.description"] = "Docker image with arm-none-eabi-gcc, cmake, gdb-multiarch and other tools for embedded development"
    return labels


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--operation", "-o",
        help="operation to perform, can be one of: build, run, stop, test", 
        choices=["build", "run", "stop", "test", "push"],
        action="append", nargs="+", required=True)

    parser.add_argument("--user", help="sets the username for the image user, defaults to current user if ommited", default="developer")
    parser.add_argument("--uid", help="sets the uid for the image user, defaults to current user if ommited", default=os.getuid())
    parser.add_argument("--gid", help="sets the gid for the image user, defaults to current user if ommited", default=os.getgid())

    parser.add_argument("--tag", help="defines the tag for the image", default=default_tag)
    args = parser.parse_args()
    print(f"Arguments: operation == {args.operation}")
    print(f"full args: {args}")    
    repo_root = get_repo_root()

    client = docker.from_env()
    
    if "stop" in args.operation[0]:
        print(f"stopping all containers with image = {default_tag}")
        containers = client.containers.list(all=True, filters={"ancestor": f"{default_tag}"})
        for c in containers:
            print(f"container: {c.id}")
            c.stop()
        print("Stopped all containers")

    if "build" in args.operation[0]:
        buildsystem_dir = repo_root
        from version import get_version
        version = get_version(os.path.join(repo_root, "version"))
        print(f"building image in {buildsystem_dir}, tagging with: {args.tag}:{version}")
        try:
            build_image(tag=f"{args.tag}:{version}", user=args.user, uid=args.uid, gid=args.gid, labels=get_labels())
        except Exception as err:
            print(f"error on build: {err}")
            sys.exit(1)

    if "run" in args.operation[0]:
        from docker.types import Mount
        repo_mount = Mount(target=f"/home/{args.user}/code", source=repo_root, type='bind')
        result = client.containers.run(image=f"{args.tag}", detach=True, stdin_open=True, stdout=True, mounts=[repo_mount],remove=False)
        print(result.logs())
        print(f"container is running with the name: {result.name}, enter bash with:")
        print(f"docker exec -it {result.name} bash")

    if "test" in args.operation[0]:
        run_tests(tag=args.tag)

    print("Done, exiting")