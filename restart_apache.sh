#!/bin/bash

c:/apache24/bin/httpd -k restart >> ${DJANGO_HOME}/restart_apache.log 2>&1
exit 0
