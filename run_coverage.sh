#!/bin/bash -i

coverage run run_tests.py
coverage html
start htmlcov/index.html
