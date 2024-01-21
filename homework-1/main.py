"""Скрипт для заполнения данными таблиц в БД Postgres."""

import psycopg2
import csv

database = "north"  # Название БД
user = "postgres"  # Название пользователя БД
password = "enoagnzc"  # сюда пароль от твоего пользователя

data = {
    "customers": "customers_data.csv",
    "employees": "employees_data.csv",
    "orders": "orders_data.csv",
}
# Путь к CSV-файлам
csv_file_path = './north_data/'

with psycopg2.connect(
        host="localhost",
        database=database,
        user=user,
        password=password
) as conn:
    with conn.cursor() as cursor:
        for table, path in data.items():
            with open(f"{csv_file_path}/{path}", 'r') as file:
                reader = csv.DictReader(file)
                fields = reader.fieldnames
                insert_query = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(['%s' for _ in fields])})"
                for row in reader:
                    cursor.execute(insert_query, tuple(row[field] for field in fields))
    conn.commit()

# INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(['%s' for _ in fields])})
# INSERT INTO {table} ('customer_id','company_name','contact_name') VALUES ('%s','%','%s')