#!/bin/sh

pip3 install virtualenv

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirement.txt