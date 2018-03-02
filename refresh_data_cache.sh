echo "start refresh $(date)" >> data_cache.log 2>&1
python manage.py refresh_data_cache >> data_cache.log 2>&1
curl --max-time 60 -X POST "https://apis.detroitmi.gov/data_cache/refresh/" >> data_cache.log 2>&1
