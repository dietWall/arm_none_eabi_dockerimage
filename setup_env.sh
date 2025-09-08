#! /usr/bin/bash

set -e

echo "Initializing Dev Environment"
echo "Creating python virtual Environment in buildsystem/venv/"

repo_root=$(git rev-parse --show-toplevel)
venv_dir=$repo_root/venv/

echo Repository located in $repo_root
echo Creating Python Virtual environment: $venv_dir
python3 -m venv $venv_dir
echo "venv created, activating"
source $venv_dir/bin/activate

echo "installing host requirements"
pip3 install -r $repo_root/requirements_host.txt

echo "requirements installed, start building docker image"

$repo_root/container_operations.py --build

echo "done"
