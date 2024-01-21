from dotenv import load_dotenv
import json
import os
import boto3
from pymongo import MongoClient
import datetime


load_dotenv()
AWS_URL = os.getenv('AWS_URL')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
MONGO_URL = os.getenv('MONGO_URL')
MONGO_DB = os.getenv('MONGO_INITDB_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')


def generate_prefix():
    dt = datetime.datetime.now() - datetime.timedelta(minutes=5)
    formatted_min = dt.minute - (dt.minute % 5)

    return f"{dt.year}/{dt.month}/{dt.day}/{dt.hour}/"\
        f"{formatted_min}"


def save_to_db():
    # initialize documnent list
    ais_location_documnents = []

    # get mongo collection `ais_location`
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    ais_location = db['ais_location']

    # get s3 resource
    s3 = boto3.resource(
        's3',
        endpoint_url=AWS_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    ais_bucket = s3.Bucket(AWS_BUCKET_NAME) 

    prefix = generate_prefix()

    for ais_bucket_object in ais_bucket.objects.filter(Prefix=prefix):
        # get MMSI from S3 object key
        *_, json_file_name = ais_bucket_object.key.split("/")
        mmsi, _ = json_file_name.split("_")

        # get location data from S3 object
        ais_object_body = ais_bucket_object.get().get('Body')
        location_data = json.loads(ais_object_body.read().decode('utf-8'))

        # put localtion data into documnents list
        ais_location_documnents.append(
            {
                "mmsi": mmsi,
                "time": location_data['time'],
                "lat": location_data['lat'],
                "lon": location_data['lon']
            }
        )

    # if documnent list is not empty insert it to MongoDB
    if len(ais_location_documnents) > 0:
        try:
            result = ais_location.insert_many(ais_location_documnents)
            print(result.inserted_ids)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    save_to_db()
