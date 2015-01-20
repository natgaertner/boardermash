from postgres_conn import get_connection
from psycopg2.extras import DictCursor
import redis
import json
import os
import csv

def get_players():
    conn = get_connection(os.getenv('POSTGRES_DB'))
    sql = "SELECT name from players order by score asc, random()"
    curs = conn.cursor(cursor_factory=DictCursor)
    curs.execute(sql)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    players_ordered = [row['name'] for row in curs.fetchall()]
    r.set('ordered_players', json.dumps(players_ordered))

def get_avs():
    with open('static/csv/has_av_map.csv') as f:
        has_av_map = csv.DictReader(f)
        r = redis.StrictRedis(host='localhost',port=6379,db=1)
        for row in has_av_map:
            r.set(row['username'],row['userid'])

if __name__ == '__main__':
    get_players()
    get_avs()
