import sys
import pandas as pd
from sqlalchemy import create_engine

# Підключення до бази даних
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# Читаємо CSV файл частинами
df_iter = pd.read_csv(
    'yellow_tripdata_2021-01.csv.gz',
    iterator=True,
    chunksize=100000
)

# Перша частина — створюємо таблицю
df = next(df_iter)

# Перетворюємо дати
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

# Створюємо таблицю в базі (тільки заголовки)
df.head(0).to_sql(
    name='yellow_taxi_data',
    con=engine,
    if_exists='replace'
)

# Записуємо перші 100,000 рядків
df.to_sql(
    name='yellow_taxi_data',
    con=engine,
    if_exists='append'
)

print("Перший chunk записано!")

# Записуємо решту даних
for chunk in df_iter:
    chunk.tpep_pickup_datetime = pd.to_datetime(chunk.tpep_pickup_datetime)
    chunk.tpep_dropoff_datetime = pd.to_datetime(chunk.tpep_dropoff_datetime)
    chunk.to_sql(
        name='yellow_taxi_data',
        con=engine,
        if_exists='append'
    )
    print("Ще один chunk записано!")

print("Всі дані завантажені!")

