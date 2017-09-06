# django_apps

  Codebase for City of Detroit DoIT web team APIs.  Implemented in Django Rest Framework.

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

# Steps to Deploy to a Server:

  * commit and push your changes to the github remote repository https://github.com/CityOfDetroit/django_apps.git

  * connect via VPN to the server

  * open git bash with administrator privileges (right click on 'git bash' and choose 'run as administrator')

  * in git bash, cd to $DJANGO_HOME and pull your changes from the remote repository:

    - `git fetch; git pull`

  * restart apache on the server:

    - `c:/apache24/bin/httpd -k restart`

# Useful custom django admin commands

  These are commands that can be run via the django_apps codebase, with the same syntax as running a local debug server (`python manage.py runserver`) except that you substitute the name of the command for 'runserver' (note that to run these you should be in either DOS or git bash, in whatever directory $DJANGO_HOME points to):

  * export_data_csv

    - Exports all the data belonging to the given model, in the given database, to a csv file:

        Usage is 'python manage.py export_data_csv <database> <model>''
        e.g., `python manage.py export_data_csv photo_survey Survey`
