dateval=$(date +%Y%m%d)

output_file="bridging_neighborhoods_favorites_${dateval}.csv"

python manage.py export_bn_data ${output_file}

mv ${output_file} s:/HRD/
