coverage run run_tests.py
if [ $? != 0 ]
then
    echo "One or more tests failed"
    exit 1
fi
coverage html
start htmlcov/index.html
