import csv
import os

import psycopg2
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = os.path.join(
    settings.BASE_DIR, 'ingredients.csv')
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD')
)
cur = conn.cursor()

with open(CSV_FILE, 'r', encoding='utf-8') as f:
    fields = ('name', 'measurement_unit', )
    dr = csv.DictReader(f, fieldnames=fields)
    to_db = [(i['name'], i['measurement_unit']) for i in dr]
cur.executemany(
    'INSERT INTO recipe_catalogue_ingredient '
    '(name, measurement_unit) VALUES (%s, %s);', to_db
)
conn.commit()
conn.close()
