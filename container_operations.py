#! /usr/bin/env python3

import docker
import argparse
import os

from git_utils import *

default_tag="stm32"


def get_container():
    client = docker.from_env()
    containers = client.containers.list(all=True, filters={"ancestor": f"{default_tag}"})
    print(f"{len(containers)} of containers found with image: {default_tag}")
    if len(containers) == 0:
        raise Exception(f"No containers found with image: {default_tag}, please start one with --run")
    if len(containers) > 1:
        print(f"WARN: Multiple containers found with image: {default_tag}, using the first one, id: {containers[0].id}")
    return containers[0]

def run_tests():
    repo_root = get_repo_root()
    #call pytest on host with container id
    import pytest
    retcode = pytest.main(["-v", "-s", f"{repo_root}/test"])
    if retcode != 0:
        raise Exception(f"Tests failed with code: {retcode}")
    print("All tests passed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #next time an operation is added, make it a list, eg something like: --operation build run test stop
    parser.add_argument("--build", help="builds the image", action='store_true',default=False)
    parser.add_argument("--run", help="starts the container", action='store_true', default=False)
    parser.add_argument("--stop", help=f"stopps any containers with the tag: {default_tag}", action='store_true', default=False)
    parser.add_argument("--test", help="runs the tests", action='store_true', default=False)

    parser.add_argument("--user", help="sets the username for the image user, defaults to current user if ommited", default="developer")
    parser.add_argument("--uid", help="sets the uid for the image user, defaults to current user if ommited", default=os.getuid())
    parser.add_argument("--gid", help="sets the gid for the image user, defaults to current user if ommited", default=os.getgid())
    parser.add_argument("--tag", help="defines the tag for the image", default=default_tag)
    args = parser.parse_args()
    repo_root = get_repo_root()
    client = docker.from_env()
    
    if args.stop == True:
        print(f"stopping all containers with image = {default_tag}")
        containers = client.containers.list(all=True, filters={"ancestor": f"{default_tag}"})
        for c in containers:
            print(f"container: {c.id}")
            c.stop()
        print("Stopped all containers")
        

    if args.build == True:    
        buildsystem_dir = repo_root
        print(f"building image in {buildsystem_dir}, tagging with: {args.tag}")
        try:
            image, build_logs = client.images.build(path=buildsystem_dir, tag=f"{args.tag}", buildargs={"user":args.user, "uid": f"{args.uid}", "gid":f"{args.gid}"})
            # for streaming the logs in realtime, we need to use client.build instead of client.images.build, as of now it is good enough
            # this one buffers and prints it afterwards
            for chunk in build_logs:
                if 'stream' in chunk:
                    for line in chunk['stream'].splitlines():
                        print(line)
            print(f"Built image with id: {image.id}")
        except Exception as err:
            print(f"error on build: {err}")
                

    if args.run == True:
        from docker.types import Mount
        repo_mount = Mount(target=f"/home/{args.user}/code", source=repo_root, type='bind')
        result = client.containers.run(image=f"{args.tag}", detach=True, stdin_open=True, stdout=True, mounts=[repo_mount],remove=True)
        print(result.logs())
        print(f"container is running with the name: {result.name}, enter bash with:")
        print(f"docker exec -it {result.name} bash")

    if args.test == True:
        run_tests()

    print("Done, exiting")