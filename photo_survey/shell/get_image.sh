if [ $# != 1 ]
then
    echo "usage: get_image.sh <image_id>"
    exit 1
fi

image_id=$1
buffer=$(curl "http://apis.detroitmi.gov/photo_survey/image/${image_id}/")

buffer=${buffer%\"}
buffer=${buffer#\"}

echo $buffer | base64 --decode > image.jpg
start image.jpg