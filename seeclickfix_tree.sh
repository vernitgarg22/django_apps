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

ILLEGAL_DUMPING_ID=6636

URL="https://${SERVER}/api/v2/request_types/${ILLEGAL_DUMPING_ID}"

curl ${URL} -o output.json
cat output.json

# Step 3: create an issue

# Use test server during testing
SERVER="test.seeclickfix.com"
# ANSWERS="{\"lat\":${LAT},\"lng\":${LNG},\"address\":\"1301 3rd ave, Detroit, MI\",\"request_type_id\":8645,\"answers\":{\"summary\":\"Testing Only - not real issue\",\"description\":\"Testing\"}"
URL="https://${SERVER}/api/v2/issues"

echo ""
echo ""
echo ${ANSWERS}

curl   -u "karl.kaebnick@gmail.com:Frei3425" -i \
       --header "Content-Type: application/json" \
       --data '{
         "lat": 42.3302,
         "lng": -83.0582,
         "address": "1301 3rd ave, Detroit, MI",
         "request_type_id": 6636,
         "answers": {
           "summary": "Testing Only - not real issue",
           "description": "Testing",
           "7500": "Yes",
           "7501": "Berm"
         }
       }' \
       -X POST https://test.seeclickfix.com/api/v2/issues -o output.html

cat output.html
exit 0
