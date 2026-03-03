from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
# Install S3 sensor if you want to use it for checking file availability in S3
# from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

# initialize DAG arguments
default_args = {
    'owner': 'tima',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 2.(Transformation)
def clean_sensor_data_logic(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['voltage'] = df['voltage'].fillna(df['voltage'].mean())
    cleaned_df = df[df['voltage'] < 400]
    return cleaned_df

def process_sensor_data():
    # simulated raw data (dictionary) from sensors
    raw_data = {
        'sensor_id': [101, 101, 102, 103],
        'voltage': [220.5, None, 230.0, 500.0], # One missing value and one outlier
        'timestamp': ['2026-03-01 10:00', '2026-03-01 10:05', '2026-03-01 10:10', '2026-03-01 10:15']
    }
    df = pd.DataFrame(raw_data)
    
    # # convert timestamp to datetime
    # df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # # fill missing values with mean voltage
    # df['voltage'] = df['voltage'].fillna(df['voltage'].mean())
    
    # # remove outliers (voltage > 400)
    # df = df[df['voltage'] < 400]
    
    cleaned_df = clean_sensor_data_logic(df)

    
    # connect to PostgreSQL and save cleaned data
    engine = create_engine('postgresql://airflow:airflow@postgres/sensor_db')
    cleaned_df.to_sql('cleaned_sensor_data', engine, if_exists='append', index=False) # Do not write Pandas index to DB
    print("Data Processed and Saved Successfully!")

# 3. define the DAG and tasks
with DAG(
    'sensor_cleaning_pipeline',
    default_args=default_args,
    description='A simple ETL for sensors',
    schedule=timedelta(days=1), # daily schedule
    catchup=False
) as dag:
    
    # --- S3 SENSOR SECTION (FUTURE USE) ---
    # For event mode, you can use the S3KeySensor to wait for the sensor data file to be uploaded to S3 before processing it.
    """wait_for_s3_file = S3KeySensor(
        task_id='wait_for_sensor_data',
        bucket_name='ind-tech-sensor-data',
        bucket_key='daily_uploads/sensor_*.csv',
        wildcard=True,
        aws_conn_id='aws_default',
        timeout=18 * 60 * 60, # wait up to 18 hours for the file to arrive
        poke_interval=60,      # check every 60 seconds
    )"""

    # define the task to process sensor data
    clean_task = PythonOperator(
        task_id='clean_and_load_sensor_data',
        python_callable=process_sensor_data
    )
    
    # If using S3 sensor, set the dependency to ensure processing happens after file is available
    # wait_for_s3_file >> clean_task

    clean_task