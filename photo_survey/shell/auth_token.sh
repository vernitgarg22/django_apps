protocol="http://"
server="localhost:8000"
echo ${server}
url="${protocol}${server}/photo_survey/auth_token/"
echo ${url}
curl -X POST -d "email=lennon@thebeatles.com&password=johnpassword" "${url}"
