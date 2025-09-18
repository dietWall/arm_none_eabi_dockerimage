#! /usr/bin/env python3

import docker
import argparse
import os

from git_utils import *

default_tag="stm32"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", help="builds the image", action='store_true',default=False)
    parser.add_argument("--run", help="starts the container", action='store_true', default=False)
    parser.add_argument("--stop", help=f"stopps any containers with the tag: {default_tag}", action='store_true', default=False)
    parser.add_argument("--user", help="sets the username for the image user, defaults to current user if ommited", default="developer")
    parser.add_argument("--uid", help="sets the uid for the image user, defaults to current user if ommited", default=os.getuid())
    parser.add_argument("--gid", help="sets the gid for the image user, defaults to current user if ommited", default=os.getgid())

    parser.add_argument("--tag", help="defines the tag for the image", default=default_tag)
    args = parser.parse_args()
    print(f"Arguments: stop == {args.stop},  build == {args.build}, run == {args.run}")
    print(f"full args: {args}")
    
    repo_root = get_repo_root()
    print(f"Repository root is: {repo_root}")

    client = docker.from_env()
    
    if args.stop == True:
        print(f"stopping all containers with image = {default_tag}:1.0")
        containers = client.containers.list(all=True, filters={"ancestor": f"{default_tag}:1.0"})
        for c in containers:
            print(f"container: {c.id}")
            c.stop()
        print("Stopped all containers")
        

    if args.build == True:    
        buildsystem_dir = repo_root
        print(f"building image in {buildsystem_dir}, tagging with: {args.tag}")
        client.images.build(path=buildsystem_dir, tag=f"{args.tag}", buildargs={"user":args.user, "uid": f"{args.uid}", "gid":f"{args.gid}"})

    if args.run == True:
        from docker.types import Mount
        repo_mount = Mount(target=f"/home/{args.user}/code", source=repo_root, type='bind')
        result = client.containers.run(image=f"{args.tag}:1.0", detach=True, stdin_open=True, stdout=True, mounts=[repo_mount],remove=True)
        print(result.logs())
        print(f"container is running with the name: {result.name}, enter bash with:")
        print(f"docker exec -it {result.name} bash")

    print("Done, exiting")