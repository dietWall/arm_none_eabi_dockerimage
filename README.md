This repo builds a docker image with arm-none-eabi installed.

# Prerequisites
You need:
- linux host with docker, python3, pip and git installed


# Usage

- clone the repo
- run setup_env.sh
  This creates an virtual environment, installs some python libs
  Builds the image
- run container_operations.py --run
  this starts a container in the background.

Once its done, you can define a .devcontainer file, which describes the image for vscode
  
