import pandas as pd
from sqlalchemy import create_engine

# Параметры подключения
DB_USER = 'myuser'
DB_PASSWORD = 'mysecretpassword'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'mydatabase'

# Путь к CSV-файлу
CSV_PATH = 'all_flats.csv'

# Создаем строку подключения
connection_string = (
    f'postgresql://{DB_USER}:{DB_PASSWORD}@'
    f'{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

# Создаем engine
engine = create_engine(connection_string)

# Читаем CSV
df = pd.read_csv(CSV_PATH)

# Заменяем NaN на None для корректной загрузки NULL
df = df.where(pd.notnull(df), None)

# Загружаем в таблицу (предполагается, что таблица 'real_estate' уже создана)
df.to_sql(
    name='real_estate',
    con=engine,
    if_exists='append',  # 'append' добавит данные, 'replace' перезапишет таблицу
    index=False,
    method='multi',
    dtype={
        'total_meters': pd.Float64Dtype(),
        'price': pd.Int64Dtype(),
        'price_per_month': pd.Int64Dtype(),
        'commissions': pd.Int64Dtype()
    }
)

print("Данные успешно загружены в PostgreSQL!")