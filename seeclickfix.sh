# Step 1: query for a report form by location.

LAT="42.3302560"
LNG="-83.0582740"

SERVER="test.seeclickfix.com"

# SERVER="en.seeclickfix.com"

# Get list of types of issues to report
URL="https://${SERVER}/api/v2/issues/new?lat=${LAT}&lng=${LNG}"

curl ${URL} -o output.json
cat output.json

echo ""
echo ""

# Step 2: query the fields for the request type. 

# ILLEGAL_DUMPING_ID=8645
ILLEGAL_DUMPING_ID=8338

URL="https://${SERVER}/api/v2/request_types/${ILLEGAL_DUMPING_ID}"

curl ${URL} -o output.json
cat output.json

# Step 3: create an issue

# Use test server during testing
SERVER="test.seeclickfix.com"
ANSWERS="{\"lat\":${LAT},\"lng\":${LNG},\"address\":\"1301 3rd ave, Detroit, MI\",\"request_type_id\":8645,\"answers\":{\"summary\":\"Testing Only - not real issue\",\"description\":\"Testing\"}"
URL="https://${SERVER}/api/v2/issues"

echo ""
echo ""
echo ${ANSWERS}

# curl -i \
#        --header "Content-Type: application/json" \
#        --data "${ANSWERS}" \
#        ${URL} -o output.html

# cat output.html
curl   -u "karl.kaebnick@gmail.com:Frei3425" -i \
       --header "Content-Type: application/json" \
       --data '{
         "lat": 42.3302,
         "lng": -83.0582,
         "address": "1301 3rd ave, Detroit, MI",
         "request_type_id": 8338,
         "answers": {
           "summary": "Testing Only - not real issue",
           "description": "Testing"
         }
       }' \
       -X POST https://test.seeclickfix.com/api/v2/issues -o output.html

# curl   -u "karl.kaebnick@gmail.com:Frei3425" -i \
#        --header "Content-Type: application/json" \
#        --data '{
#          "lat": 42.3302,
#          "lng": -83.0582,
#          "address": "1301 3rd ave, Detroit, MI",
#          "request_type_id": 8645,
#          "answers": {
#            "summary": "Testing Only - not real issue",
#            "description": "Testing",
#            "9368": "Yes",
#            "9369": "No",
#            "9370": "tires",
#            "9371": "Front Yard"
#          }
#        }' \
#        -X POST https://test.seeclickfix.com/api/v2/issues -o output.html

cat output.html
exit 0


6636


curl   -u "karl.kaebnick@gmail.com:Frei3425" -i \
       --header "Content-Type: application/json" \
       --data '{
         "lat": 42.3302,
         "lng": -83.0582,
         "address": "1301 3rd ave, Detroit, MI",
         "request_type_id": 8645,
         "answers": {
           "summary": "Testing Only - not real issue",
           "description": "Testing",
           "9368": "Yes",
           "9369": "No",
           "9370": "tires",
           "9371": "Front Yard"
         }
       }' \
       -X POST https://test.seeclickfix.com/api/v2/issues -o output.html

cat output.html
exit 0

curl -u "karl.kaebnick@gmail.com:Frei3425" -i \
       --header "Content-Type: application/json" \
       --data '{
         "lat": 42.3302560,
         "lng": -83.0582740,
         "address": "123 State St. New Haven, CT",
         "request_type_id": 8645,
         "answers": {
           "142": "SHALLOW",
           "summary": "Big Pothole",
           "description": "Please fix it"
         }
       }' \
       https://seeclickfix.com/api/v2/issues
