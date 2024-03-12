# importing required libraries

from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd
import json


# defining functions
def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit

def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids="extract_weather_data")
    city = data["name"]
    weather_description = data["weather"][0]['description']
    temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp"])
    feels_like_farenheit= kelvin_to_fahrenheit(data["main"]["feels_like"])
    min_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
    max_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    transformed_data = {"City": city,
                        "Description": weather_description,
                        "Temperature (F)": temp_farenheit,
                        "Feels Like (F)": feels_like_farenheit,
                        "Minimun Temp (F)":min_temp_farenheit,
                        "Maximum Temp (F)": max_temp_farenheit,
                        "Pressure": pressure,
                        "Humidty": humidity,
                        "Wind Speed": wind_speed,
                        "Time of Record": time_of_record,
                        "Sunrise (Local Time)":sunrise_time,
                        "Sunset (Local Time)": sunset_time                        
                        }
    
    # storing the dictionary transformed_data into a pandas dataframe
    df = pd.DataFrame([transformed_data])

    # below lines of code are to find the current-time while exporting the dataframe into a csv file and storing it
    # into amazon s3 bucket
    # file name example : current_weather_data_Chicago_timestampvalue.csv
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = f'current_weather_data_{city}_' + dt_string


    df.to_csv(f"s3://yours3bucketname/{dt_string}.csv", index=False)


# defining the default arguments for airflow 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 11),
    'email': ['abc@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

api_key = 'your_openweathermap_api_key'
city = 'Chicago'


# defining the DAG

with DAG(
    'open_weather_api',
    default_args=default_args,
    schedule_interval = '@daily',
    catchup = False
    ) as dag:

    is_weather_api_ready = HttpSensor(
        task_id ='is_weather_api_ready',
        http_conn_id ='weathermap_api',
        endpoint = f'/data/2.5/weather?q={city}&APPID={api_key}'
    )

    extract_weather_data = SimpleHttpOperator(
        task_id = 'extract_weather_data',
        http_conn_id = 'weathermap_api',
        endpoint = f'/data/2.5/weather?q={city}&APPID={api_key}',
        method = 'GET',
        response_filter = lambda r: json.loads(r.text),
        log_response = True
        )

    transform_load_weather_data = PythonOperator(
        task_id = 'transform_load_weather_data',
        python_callable = transform_load_data
        )

    is_weather_api_ready >> extract_weather_data >> transform_load_weather_data