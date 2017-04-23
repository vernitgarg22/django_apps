OUTPUT="${DJANGO_HOME}/waste_notifier_output.txt"

echo $(date) >> ${OUTPUT}
date_str=$(date "+%Y%m%d")
url="https://apis.detroitmi.gov/waste_notifier/send/?today=${date_str}"
curl -X POST ${url} >> ${OUTPUT}
err_code=$?
echo "" >> ${OUTPUT}
echo "error code: ${err_code}" >> ${OUTPUT}
echo "" >> ${OUTPUT}
