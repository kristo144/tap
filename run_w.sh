#!/bin/sh

python -m venv venv
. venv/Scripts/activate
pip install mcpi pytest pytest-cov
python demo.py