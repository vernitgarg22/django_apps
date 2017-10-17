coverage run run_tests.py
if [ $? != 0 ]
then
    echo "One or more tests failed"
    exit 1
fi
coverage html
which start > /dev/null
retval=$?
if [ ${retval} -eq 0 ]
then
	start htmlcov/index.html
else
	open htmlcov/index.html
fi
