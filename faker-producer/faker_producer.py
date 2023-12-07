import asyncio
import configparser
import os
import time
from collections import namedtuple
from kafka import KafkaProducer
from faker import Faker
import json
from datetime import date

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))

fake = Faker()

#generate more than 10 different fields
def get_registered_user():
    return {
        "id": str(fake.uuid4()),
        "name": fake.name(),
        "address": fake.address(),
        "year": fake.year(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "job": fake.job(),
        "company": fake.company(),
        "date_of_birth": fake.date_of_birth(),
        "city": fake.city(),
        "country": fake.country(),
        "text": fake.text(),
        "sentence": fake.sentence(),
        "word": fake.word(),
        "color": fake.color_name(),
        "credit_card_number": fake.credit_card_number(),
        "ipv4": fake.ipv4(),
    }

def serialize_date(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def run():
    iterator = 0
    print("Setting up Faker producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x, default=serialize_date).encode('utf-8'),
    )

    while True:
        sendit = get_registered_user()
        # adding prints for debugging in logs
        print("Sending new faker data iteration - {}".format(iterator))
        producer.send(TOPIC_NAME, value=sendit)
        print("New faker data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up lmao!")
        iterator += 1


if __name__ == "__main__":
    run()