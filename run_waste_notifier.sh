OUTPUT="${DJANGO_HOME}/waste_notifier_output.txt"

echo $(date) >> ${OUTPUT}
curl --silent https://apis.detroitmi.gov/waste_notifier/send/ >> ${OUTPUT}
echo "" >> ${OUTPUT}

