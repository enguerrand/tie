#!/bin/bash
cd $(dirname $0)/..
export PYTHONPATH=.
python3 tests/manual_frontend_test.py