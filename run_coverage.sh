#!/usr/bin/env bash

coverage run run_tests.py
coverage html
start ./htmlcov/index.html
