#!/bin/bash

apt install python3 python3-pip python3-venv
pip3 install virtualenv

python3 -m venv .venv

. .venv/bin/activate

pip3 install -r requirements.txt -r dev-requirements.txt
pip3 install -e .
exit 0