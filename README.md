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

  * export_data_csv - Exports all the data belonging to the given model, in the given database, to a csv file:

    - Usage: 'python manage.py export_data_csv <database> <model>'<br/>
    e.g., `python manage.py export_data_csv photo_survey Survey`

  * import_assessors_data - Imports assessors data into finassessorprod or warehousedb1.

    - Usage: 'python manage.py import_assessors_data <database> <csv_file>'<br/>
    e.g., `python manage.py import_assessors_data finassessorprod MTT_TRACKEREXPORT2018.csv`

  * export_survey_answers - Exports photo_survey survey results to a csv file for a given type of survey.

    - Usage: 'python manage.py export_survey_answers survey_template_id'<br/>
    e.g., `python manage.py export_survey_answers default_combined`

    - optional parameters:

      `--pretty_print=y|n` (Pretty print values? Default: 'y')

      `--remove_dupes=y|n` (Only return most-recent survey for each parcel? Default: 'y')

      `--add_data='ownership,address_info'` (Comma-delimited set of types of data to add. Default: 'ownership,address_info')

      `--calc_score=y|n` (Calculate a score for each survey? Default: 'y')

      `--add_streetview_link=y|n` (Add a link to mapillary streetview? Default: 'y')

  * import_image_metadata - Import image metadata from a csv file into the photo survey database.

    - Usage: 'python manage.py import_image_metadata <file_path> <database>'<br/>
    e.g., `python manage.py import_image_metadata survey_20170720.csv photo_survey_dev`

  * send_message - Sends a text message to a given phone number (useful for replying to waste notification feedback & questions).
    
    - Usage: 'python manage.py send_message <phone number> <text message>'<br/>
    e.g., `python manage.py send_message '2125799232' 'Sample text message'`
