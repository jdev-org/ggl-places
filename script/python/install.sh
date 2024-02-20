#!/bin/bash

echo "INSTALL.....START"

env_py_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo $env_py_dir

# Install OS packages
apt install python3 python3-pip python3-venv gdal-bin
# Install virtualenv python package
pip3 install virtualenv

if [ -d "$env_py_dir/.venv" ]; then
  echo "INSTALL.....ALREADY INSTALLED.....CONTINUE....."
else
    python3 -m venv "$env_py_dir/.venv"
    . "$env_py_dir/.venv/bin/activate"
    pip3 install -r "$env_py_dir/requirements.txt" -r "$env_py_dir/dev-requirements.txt"
    pip3 install -e "$env_py_dir"
    deactivate
fi
echo "INSTALL.....FINISH"