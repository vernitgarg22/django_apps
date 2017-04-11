OUTPUT="c:/cygwin64/home/kaebnickk/output.txt"

echo $(date) >> ${OUTPUT}
curl --silent https://apis.detroitmi.gov/waste_notifier/send/ >> ${OUTPUT}
echo "" >> ${OUTPUT}

