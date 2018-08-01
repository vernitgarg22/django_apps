#!/usr/bin/env python
import subprocess

def run_cmd(cmd, errmsg, fallback=None):

    return_value = subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)
    if return_value.returncode == 0:
        return True
    if fallback:
        return run_cmd(cmd=fallback, errmsg=errmsg)
    else:
        raise Exception(errmsg)

run_cmd(cmd="coverage run run_tests.py", errmsg="One or more tests failed")
run_cmd(cmd="coverage html", errmsg="Error generating coverage html")
run_cmd(cmd="start htmlcov/index.html", fallback="coverage report", errmsg="Error opening coverage report")
