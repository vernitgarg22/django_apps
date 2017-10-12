OUTPUT="${DJANGO_HOME}/waste_notifier_output.txt"

echo $(date) >> ${OUTPUT}
echo "" >> ${OUTPUT}
python manage.py send_waste_reminders >> ${OUTPUT} 2>&1
echo "" >> ${OUTPUT}
