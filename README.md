This repo builds a docker image with arm-none-eabi installed.
This image is used for building STM32 related applications and libraries.
I´m not sure if this is ready for release yet, so the package is private yet.
If you want to use it, don´t hesitate to contact me. I will publish/release the package.


# Prerequisites
You need:
- A Linux PC (or WSL) with git, docker, python3 with venv and a package manager
All other tools should be installed and configured automatically (in theory, please contact me if something fails).
- your user must be configured to run docker commands without sudo: https://docs.docker.com/engine/install/linux-postinstall


# Usage for compilation
- pull the image:
```bash
docker pull ghcr.io/dietwall/arm_gcc_image:latest
```
- run setup_env.sh on host
  This creates an virtual environment, installs missing python libs in venv and builds the docker image

```bash
./setup_env.sh
```
- You can test the container by running 
```bash
source venv/bin/activate
./container_operations.py -o run
```
this starts a container in the background, leaves it running, so you can enter it with common docker commands (one is printed at the end of the operation).  

Optionally run:
```bash
./container_operations.py -o run test
```
to run a simple compilation test.

## container_operations.py
This is the main script, that implements some operations for handling the images and containers. 

Other options for container_operations.py, all are optional and have defaults set:  
--tag [IMAGE_TAG] : overrides the default tag for the image  
--user [USERNAME] : provides a username for the image, default=developer   
--uid [UID] : provides a uid for the docker image, default is the currently logged in user (required for github runners as an example)  
--gid [UID] : provides a group id for the docker image, default is the currently logged in user    

## Other Operations:  
all operations/actions have to be preceded with a single --operation / -o  
build: builds the image   
stop: stops all container with the default (or provided with --tag) tag  
test: starts a pytest process that compiles a small application in the container (container must be already running!)  
push: used in github actions for publishing  
save: saves the image to a tar file (used in github actions)   
run: starts a detached container and leaves it running  

The Image is reused in different repositories by copying template/devcontainer.json to <repo-root>/.devcontainer/devcontainer.json. If VsCode has the the Dev Containers installed, it will ask you if you want to reopen this in the container.


## Developing applications:
This is my base image, so if you want to use it for developing applications, it should be enriched with required libraries.  
On my other repos you will probably find some more useful images with HAL/RTOS installed. So the applications can easily link to this libs.    

However:
You need VSCode with devcontainer extension installed: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

After copying/creating devcontainer file, you need to open your repository root directory and run vscode. If everything works out, you should see a notification whether you want to reopen the directory inside the devcontainer.

  
