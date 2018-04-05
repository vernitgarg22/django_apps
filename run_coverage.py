#!/usr/bin/env python
import subprocess


class run_cmd():

    def __init__(self, cmd, errmsg):

        return_value = subprocess.run(cmd, shell=True)
        if return_value.returncode != 0:
            raise Exception(errmsg)

run_cmd("coverage run run_tests.py", "One or more tests failed")
run_cmd("coverage html", "Error generating coverage html")
run_cmd("start htmlcov/index.html", "Error opening coverage report")
