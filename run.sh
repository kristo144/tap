#!/bin/sh

python3 -m venv venv
source venv/bin/activate
pip install mcpi pytest pytest-cov
python3 demo.py