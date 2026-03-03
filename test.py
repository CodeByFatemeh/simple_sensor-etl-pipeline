import pandas as pd
from sqlalchemy import create_engine

try:
    # امتحان کردن یوزر اصلی پستگرس به جای یوزر ایرفلو
    # فرمت: postgresql://username:password@localhost:5432/dbname
    
    # سناریو ۱: اگر دیتای ایرفلو را می‌خواهی چک کنی:
    # engine = create_engine('postgresql://postgres:postgres_pass_ft@localhost:5432/postgres')
    
    # سناریو ۲: اگر با داکر-کمپوز بالا آوردی، یوزر و پسورد و دیتابیس هر سه airflow هستند:
    engine = create_engine('postgresql://airflow:airflow@127.0.0.1:5434/sensor_db')    # خواندن دیتا
    df = pd.read_sql("SELECT * FROM cleaned_sensor_data", engine)
    
    print("✅ ارتباط با دیتابیس برقرار شد!")
    print("--- دیتای تمیز شده سنسورها ---")
    print(df)

except Exception as e:
    print("❌ خطا در اتصال یا خواندن دیتا:")
    print(e)