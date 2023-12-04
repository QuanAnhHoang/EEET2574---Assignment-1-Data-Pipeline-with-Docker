import os
import time
import requests
from kafka import KafkaProducer
import json
from datetime import date, datetime

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))
MOCKAROO_API_KEY = os.environ.get("MOCKAROO_API_KEY", "030b6f00")  # Your Mockaroo API key
MOCKAROO_SCHEMA_ID = "d9720740"  # Replace with your Mockaroo schema ID

def get_mockaroo_data():
    # Make a request to the Mockaroo API to get fake data for one row
    url = f"https://api.mockaroo.com/api/{MOCKAROO_SCHEMA_ID}.json"
    params = {"count": 1, "key": MOCKAROO_API_KEY}
    print("Requesting URL:", url)
    print("Requesting Params:", params)
    response = requests.get(url, params=params)
    if response.status_code == 200:
        mockaroo_data = response.json()[0]

        # Convert arrival_date and departure_date to a consistent date format
        mockaroo_data['departure_date'] = convert_to_cassandra_date_format(mockaroo_data.get('departure_date'))
        mockaroo_data['arrival_date'] = convert_to_cassandra_date_format(mockaroo_data.get('arrival_date'))

        # Convert departure_time and arrival_time to the expected format
        mockaroo_data['departure_time'] = convert_to_cassandra_time_format(mockaroo_data['departure_time'])
        mockaroo_data['arrival_time'] = convert_to_cassandra_time_format(mockaroo_data['arrival_time'])

        return mockaroo_data
    else:
        print(f"Failed to fetch data from Mockaroo. Status code: {response.status_code}")
        return None

def convert_to_cassandra_date_format(date_str):
    try:
        # Convert date to a consistent format, assuming the input format is 'MM/DD/YYYY'
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        print(f"Error converting date: {date_str}")
        return None
    
def convert_to_cassandra_time_format(time_str):
    # Convert time from '1:08 PM' to '13:08:00' (24-hour format)
    time_obj = datetime.strptime(time_str, '%I:%M %p')
    return time_obj.strftime('%H:%M:%S')

def serialize_date(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def run():
    iterator = 0
    print("Setting up Mockaroo producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x, default=serialize_date).encode('utf-8'),
    )

    while True:
        mockaroo_data = get_mockaroo_data()

        if mockaroo_data:
            # adding prints for debugging in logs
            print("Sending new Mockaroo data iteration - {}".format(iterator))
            producer.send(TOPIC_NAME, value=mockaroo_data)
            print("New Mockaroo data sent")

        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1

if __name__ == "__main__":
    run()
