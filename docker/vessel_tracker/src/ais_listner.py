import asyncio
import json
from dotenv import load_dotenv
import os
import boto3
import uuid
import paho.mqtt.client as mqtt
from time import sleep 
import datetime


load_dotenv()
PERIOD = os.getenv('PERIOD')
APP_NAME = os.getenv('APP_NAME')
AWS_URL = os.getenv('AWS_URL')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
TOPIC = os.getenv('TOPIC')
DIGITRAFIC_URL = os.getenv('DIGITRAFIC_URL')

# get s3 resource
s3 = boto3.resource(
    's3',
    endpoint_url=AWS_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def on_message(client, userdata, message):
    # get MMSI from topic
    _, mmsi, _ = message.topic.split('/')

    # get location data from message payload
    payload = message.payload.decode('utf-8')
    location = json.loads(payload)

    # round minute by 5
    dt = datetime.datetime.fromtimestamp(location['time'])
    formatted_min = dt.minute - (dt.minute % 5)

    # generate S3 object key
    key = f"{dt.year}/{dt.month}/{dt.day}/{dt.hour}/"\
          f"{formatted_min}/{mmsi}_{location['time']}.json"

    # save location data to S3
    try:
        s3obj = s3.Object(AWS_BUCKET_NAME, key)
        s3obj.put(Body=payload)
    except Exception as e:
        print("Fail to save AIS PositionReport: ", e)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {rc}\n")


async def ais_subscriber():
    try:
        # create bucket if it doesn't exist 
        s3.create_bucket(Bucket=AWS_BUCKET_NAME)

        # prepare mqtt client 
        client_name = f"{APP_NAME};{str(uuid.uuid4())}"
        client = mqtt.Client(client_name, transport="websockets")

        # set mqtt client callback functions
        client.on_connect = on_connect
        client.on_message = on_message

        # connect to MQTT broker 
        client.tls_set()
        client.connect_async(DIGITRAFIC_URL, 443)

        client.loop_start()

        while True:
            # alive check
            current_datetime = datetime.datetime.now()
            print(f"{current_datetime}: listen to AIS location topic")
            sleep(3600)

    except KeyboardInterrupt:
        print('stop by keyboard interrrupt')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(ais_subscriber())
