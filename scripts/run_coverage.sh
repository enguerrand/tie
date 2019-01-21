#!/bin/bash
cd $(dirname $0)/../tests
export PYTHONPATH=..
coverage3 run --source ../lib -m unittest discover .
coverage3 report -m