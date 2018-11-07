OUTPUT="${DJANGO_HOME}/waste_notifier_output.txt"

echo $(date) >> ${OUTPUT}
echo "" >> ${OUTPUT}
python manage.py send_waste_reminders >> ${OUTPUT} 2>&1
retval=$?
echo "" >> ${OUTPUT}

if [ ${retval} -ne 0 ]
then

    python manage.py send_message '9178428901' 'Waste reminders failed'

fi

exit 0
