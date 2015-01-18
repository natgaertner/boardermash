import psycopg2 as psql
import os

def get_connection(database):
    return psql.connect(user=os.getenv('POSTGRES_USER'),password=os.getenv('POSTGRES_PW'),host=os.getenv('POSTGRES_HOST'),database=database)

