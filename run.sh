#!/bin/sh

python3 -m venv venv
. venv/bin/activate
pip install mcpi pytest pytest-cov
python3 demo.py