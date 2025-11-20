This repo builds a docker image with arm-none-eabi installed.
After building, the image can be reused to build and debug STM32 applications with devcontainer functionality from VsCode.

# Prerequisites
You need:
- A PC with Windows and Windows Subsystem for Linux (WSL) installed
- Inside WSL you need at least: git, docker, python3 with venv
All other tools should be installed and configured automatically (in theory, please contact me if something fails :) ).


# Usage

- clone the repo
```bash
git clone https://github.com/dietWall/arm_none_eabi_dockerimage && cd arm_none_eabi_dockerimage
```

- run setup_env.sh
  This creates an virtual environment, installs missing python libs in venv and starts to build the docker image
```bash
./setup_env.sh
```

- You can test the container by running 
```bash
./container_operations.py --run
```
this starts a container in the background, leaves it running, so you can enter it with common docker commands. Optionally run
```bash
./container_operations.py --run --test
```
to run a simple compilation test.

## container_operations.py
This is the main script, that implements the functionality. 

Other options for container_operations.py, all are optional and have defaults set:  
--tag IMAGE_TAG : tags the image with given argument. default is stm32  
--user USERNAME : provides a username for the image, default=developer  
--uid [UID] : provides a uid for the docker image, default is the currently logged in user  
--gid [UID] : provides a group id for the docker image, default is the currently logged in user  

## Operations:
--build: builds the image
--stop: stops all container with the default (or provided with --tag) tag

The Image can be reused in different repositories by copying template/devcontainer.json to <your-repo-root>/.devcontainer/devcontainer.json

## Developing applications:
You need VSCode with devcontainer extension installed: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

After copying/creating devcontainer file, you need to open your repository root directory and run vscode. If everything works out, you should see a notification whether you want to reopen the directory inside the devcontainer definition.

  
