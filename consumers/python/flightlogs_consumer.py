from kafka import KafkaConsumer
import os
import json


if __name__ == "__main__":
    print("Starting Flight logs Consumer")
    TOPIC_NAME = os.environ.get("TOPIC_NAME", "flightlogs")  # Adjust the topic name
    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")

    print("Setting up Kafka consumer at {}".format(KAFKA_BROKER_URL))
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_BROKER_URL])

    print('Waiting for messages...')
    for msg in consumer:
        msg_value = msg.value.decode('utf-8')
        
        try:
            jsonData = json.loads(msg_value)
            # add print for checking
            print(jsonData)
            # print keys to see which fields are present
            print("Keys in the JSON data:")
            print(jsonData.keys())
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON data. Error: {e}")
