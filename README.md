# django_apps

# Codebase for City of Detroit DoIT web team APIs.  Implemented in Django Rest Framework.

# Steps to Install:

  * make sure you have at least version 3.4 of python installed

  * (optional) install and activate [https://virtualenv.pypa.io](virtualenv)

  * clone djanga_apps repo:

    - `git clone https://github.com/CityOfDetroit/django_apps.git`

  * set an environmntal variable named `$DJANGO_HOME`

    - the value of this variable should be the path to your local copy of django_apps, e.g., `c:/users/kaebnickk/django_apps`

  * get a local copy of the machine-specific settings file (check with @karlk on how to do this)

  * use python's pip app to install required packages:

    - `pip install -r requirements.txt`

  * run unit tests from the root of django_apps:

    - `./run_coverage.py`

# Steps to Deploy:

  * commit and push your changes to the github remote repository

  * VPN to server

  * open git bash with administrator privileges

  * in git bash, cd to $DJANGO_HOME

  * execute to pull your changes from the remote repository:

    - `git fetch; git pull`

  * restart apache on the server:

    - `c:/apache24/bin/httpd -k restart`