#!/bin/bash

black --exclude test/resources .

isort --skip test/resources/ .

flake8 . --count --select=E9,F63,F7,F82 --exclude test/resources,transformations2log/__init__.py --show-source --statistics

flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --exclude test/resources,transformations2log/__init__.py --statistics

python -m unittest