CREATE TABLE weatherreport (
  forecastdate TIMESTAMP,
  location TEXT,
  description TEXT,
  temp FLOAT,
  feels_like FLOAT,
  temp_min FLOAT,
  temp_max FLOAT,
  pressure FLOAT,
  humidity FLOAT,
  wind FLOAT,
  sunrise BIGINT,
  sunset BIGINT,
  PRIMARY KEY (location, forecastdate)
);

CREATE TABLE twitterdata (
  tweet_date TIMESTAMP,
  location TEXT,
  tweet TEXT,
  classification TEXT,
  PRIMARY KEY (location, tweet_date)
);

CREATE TABLE IF NOT EXISTS fakerdata (
    id UUID PRIMARY KEY,
    address TEXT,
    city TEXT,
    color TEXT,
    company TEXT,
    country TEXT,
    credit_card_number TEXT,
    date_of_birth DATE,
    email TEXT,
    ipv4 INET,
    job TEXT,
    name TEXT,
    phone_number TEXT,
    sentence TEXT,
    text TEXT,
    word TEXT,
    year INT
);

CREATE TABLE IF NOT EXISTS flightlogsdata (
    flight_id TEXT PRIMARY KEY,
    flight_number INT,
    departure_airport TEXT,
    arrival_airport TEXT,
    departure_date DATE,
    arrival_date DATE,
    departure_time TIME,
    arrival_time TIME,
    airline TEXT,
    passenger_count INT,
    flight_duration DECIMAL
);