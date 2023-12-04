import datetime
import gzip
import os
import re
import sys

import pandas as pd
from cassandra.cluster import BatchStatement, Cluster, ConsistencyLevel
from cassandra.query import dict_factory

tablename = os.getenv("weather.table", "weatherreport")
twittertable = os.getenv("twittertable.table", "twitterdata")
fakertable = os.getenv("fakertable.table", "fakerdata")
flightlogstable = os.getenv("flightlogstable.table", "flightlogsdata")

CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST") if os.environ.get("CASSANDRA_HOST") else 'localhost'
CASSANDRA_KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE") if os.environ.get("CASSANDRA_KEYSPACE") else 'kafkapipeline'

WEATHER_TABLE = os.environ.get("WEATHER_TABLE") if os.environ.get("WEATHER_TABLE") else 'weather'
TWITTER_TABLE = os.environ.get("TWITTER_TABLE") if os.environ.get("TWITTER_TABLE") else 'twitter'
FAKER_TABLE = os.environ.get("FAKER_TABLE") if os.environ.get("FAKER_TABLE") else 'faker'
FLIGHTLOGS_TABLE = os.environ.get("FLIGHTLOGS_TABLE") if os.environ.get("FLIGHTLOGS_TABLE") else 'flightlogs'

def saveTwitterDf(dfrecords):
    if isinstance(CASSANDRA_HOST, list):
        cluster = Cluster(CASSANDRA_HOST)
    else:
        cluster = Cluster([CASSANDRA_HOST])

    session = cluster.connect(CASSANDRA_KEYSPACE)

    counter = 0
    totalcount = 0

    cqlsentence = "INSERT INTO " + twittertable + " (tweet_date, location, tweet, classification) \
                   VALUES (?, ?, ?, ?)"
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    insert = session.prepare(cqlsentence)
    batches = []
    for idx, val in dfrecords.iterrows():
        batch.add(insert, (val['datetime'], val['location'],
                           val['tweet'], val['classification']))
        counter += 1
        if counter >= 100:
            print('inserting ' + str(counter) + ' records')
            totalcount += counter
            counter = 0
            batches.append(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    if counter != 0:
        batches.append(batch)
        totalcount += counter
    rs = [session.execute(b, trace=True) for b in batches]

    print('Inserted ' + str(totalcount) + ' rows in total')


def saveFakerDf(dfrecords):
    if isinstance(CASSANDRA_HOST, list):
        cluster = Cluster(CASSANDRA_HOST)
    else:
        cluster = Cluster([CASSANDRA_HOST])

    session = cluster.connect(CASSANDRA_KEYSPACE)

    counter = 0
    totalcount = 0

    cqlsentence = "INSERT INTO " + fakertable + " (name, address, year, email, phone_number, job, company, date_of_birth, city, country, text, sentence, word, color, credit_card_number, ipv4) \
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    insert = session.prepare(cqlsentence)
    batches = []
    for idx, val in dfrecords.iterrows():
        batch.add(insert, (
            val['name'], val['address'], val['year'], val['email'], val['phone_number'],
            val['job'], val['company'], val['date_of_birth'], val['city'], val['country'],
            val['text'], val['sentence'], val['word'], val['color'], val['credit_card_number'],
            val['ipv4']
        ))
        counter += 1
        if counter >= 100:
            print('inserting ' + str(counter) + ' records')
            totalcount += counter
            counter = 0
            batches.append(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    if counter != 0:
        batches.append(batch)
        totalcount += counter
    rs = [session.execute(b, trace=True) for b in batches]

    print('Inserted ' + str(totalcount) + ' rows in total')

def saveWeatherreport(dfrecords):
    if isinstance(CASSANDRA_HOST, list):
        cluster = Cluster(CASSANDRA_HOST)
    else:
        cluster = Cluster([CASSANDRA_HOST])

    session = cluster.connect(CASSANDRA_KEYSPACE)

    counter = 0
    totalcount = 0

    cqlsentence = "INSERT INTO " + tablename + " (forecastdate, location, description, temp, feels_like, temp_min, temp_max, pressure, humidity, wind, sunrise, sunset) \
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    insert = session.prepare(cqlsentence)
    batches = []
    for idx, val in dfrecords.iterrows():
        batch.add(insert, (val['report_time'], val['location'], val['description'],
                           val['temp'], val['feels_like'], val['temp_min'], val['temp_max'],
                           val['pressure'], val['humidity'], val['wind'], val['sunrise'], val['sunset']))
        counter += 1
        if counter >= 100:
            print('inserting ' + str(counter) + ' records')
            totalcount += counter
            counter = 0
            batches.append(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    if counter != 0:
        batches.append(batch)
        totalcount += counter
    rs = [session.execute(b, trace=True) for b in batches]

    print('Inserted ' + str(totalcount) + ' rows in total')

def saveFlightLogsData(dfrecords):
    if isinstance(CASSANDRA_HOST, list):
        cluster = Cluster(CASSANDRA_HOST)
    else:
        cluster = Cluster([CASSANDRA_HOST])

    session = cluster.connect(CASSANDRA_KEYSPACE)

    counter = 0
    totalcount = 0

    cqlsentence = "INSERT INTO " + tablename + " (flight_id, flight_number, departure_airport, arrival_airport, departure_date, arrival_date, departure_time, arrival_time, airline, passenger_count, flight_duration) \
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    insert = session.prepare(cqlsentence)
    batches = []
    for idx, val in dfrecords.iterrows():
        batch.add(insert, (
            val['flight_id'], val['flight_number'], val['departure_airport'], val['arrival_airport'],
            val['departure_date'], val['arrival_date'], val['departure_time'], val['arrival_time'],
            val['airline'], val['passenger_count'], val['flight_duration']
        ))
        counter += 1
        if counter >= 100:
            print('inserting ' + str(counter) + ' records')
            totalcount += counter
            counter = 0
            batches.append(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    if counter != 0:
        batches.append(batch)
        totalcount += counter
    rs = [session.execute(b, trace=True) for b in batches]

    print('Inserted ' + str(totalcount) + ' rows in total')


def loadDF(targetfile, target):
    if target == 'weather':
        colsnames = ['description', 'temp', 'feels_like', 'temp_min', 'temp_max',
                     'pressure', 'humidity', 'wind', 'sunrise', 'sunset', 'location', 'report_time']
        dfData = pd.read_csv(targetfile, header=None,
                             parse_dates=True, names=colsnames)
        dfData['report_time'] = pd.to_datetime(dfData['report_time'])
        saveWeatherreport(dfData)
    elif target == 'twitter':
        colsnames = ['tweet', 'datetime', 'location', 'classification']
        dfData = pd.read_csv(targetfile, header=None,
                             parse_dates=True, names=colsnames)
        dfData['datetime'] = pd.to_datetime(dfData['datetime'])
        saveTwitterDf(dfData)
    elif target == 'faker':
        colsnames = ['name', 'address', 'year', 'email', 'phone_number', 'job', 'company', 'date_of_birth', 'city', 'country', 'text', 'sentence', 'word', 'color', 'credit_card_number', 'ipv4']
        dfData = pd.read_csv(targetfile, header=None,
                             parse_dates=True, names=colsnames)
        dfData['date_of_birth'] = pd.to_datetime(dfData['date_of_birth'])
        saveFakerDf(dfData)
    elif target == 'flightlogs':
        colsnames = ['flight_id', 'flight_number', 'departure_airport', 'arrival_airport',
                 'departure_date', 'arrival_date', 'departure_time', 'arrival_time',
                 'airline', 'passenger_count', 'flight_duration']
        dfData = pd.read_csv(targetfile, header=None, 
                                parse_dates=True, names=colsnames)
        dfData['departure_date'] = pd.to_datetime(dfData['departure_date'])
        dfData['arrival_date'] = pd.to_datetime(dfData['arrival_date'])
        dfData['departure_time'] = pd.to_datetime(dfData['departure_time'], format='%I:%M %p').dt.time
        dfData['arrival_time'] = pd.to_datetime(dfData['arrival_time'], format='%I:%M %p').dt.time    
        saveFlightLogsData(dfData)

def getWeatherDF():
    return getDF(WEATHER_TABLE)
def getTwitterDF():
    return getDF(TWITTER_TABLE)
def getFakerDF():
    print(FAKER_TABLE)
    return getDF(FAKER_TABLE)
def getFlightLogsDF():
    print(FLIGHTLOGS_TABLE)
    return getDF(FLIGHTLOGS_TABLE)

def getDF(source_table):
    if isinstance(CASSANDRA_HOST, list):
        cluster = Cluster(CASSANDRA_HOST)
    else:
        cluster = Cluster([CASSANDRA_HOST])

    if source_table not in (WEATHER_TABLE, TWITTER_TABLE, FAKER_TABLE, FLIGHTLOGS_TABLE):
        return None

    session = cluster.connect(CASSANDRA_KEYSPACE)
    session.row_factory = dict_factory
    cqlquery = "SELECT * FROM " + source_table + ";"
    rows = session.execute(cqlquery)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    action = sys.argv[1]
    target = sys.argv[2]
    targetfile = sys.argv[3]
    if action == "save":
        loadDF(targetfile, target)
    elif action == "get":
        getDF(target)