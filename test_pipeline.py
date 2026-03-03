import pytest
import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine

from dags.sensor_processing import clean_sensor_data_logic

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

# 1. Unit Test: testing the cleaning logic for outliers and missing values without connecting to the database
def test_clean_sensor_logic():
    raw_input = pd.DataFrame({
    'sensor_id': [1, 2, 3],
    'voltage': [200, None, 500], 
    'timestamp': ['2026-03-01', '2026-03-01', '2026-03-01']
    })
    processed_df = clean_sensor_data_logic(raw_input)

    assert len(processed_df) == 2
    assert processed_df['voltage'].isnull().sum() == 0
    assert (processed_df['voltage'] < 400).all() # Edge case test to ensure outlier is removed
    assert processed_df.iloc[1]['voltage'] == 350
    
# 2. Integration Test: tetsting the full pipeline with database connection and data insertion
@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping DB connection test in GitHub Actions")
def test_database_connection():
    try:
        engine = create_engine('postgresql://airflow:airflow@127.0.0.1:5434/sensor_db')
        connection = engine.connect()
        connection.close()
        success = True
    except Exception:
        success = False
    assert success is True
    
# 3. Data Quality Test: checking if the cleaned data in the database meets quality criteria (no outliers, no missing values)
@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping Data Quality test in GitHub Actions")
def test_final_data_quality():
    engine = create_engine('postgresql://airflow:airflow@127.0.0.1:5434/sensor_db')
    try:
        df = pd.read_sql("SELECT * FROM cleaned_sensor_data", engine)
        assert not df.empty
        # Check for expected columns and data quality
        assert 'voltage' in df.columns
        assert 'sensor_id' in df.columns
        assert df['voltage'].max() < 400
        assert len(df.columns) == 3
    except Exception as e:
        pytest.fail(f"Table not found or error: {e}")