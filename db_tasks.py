from postgres_conn import get_connection
from mash_calc import calc_rating
from psycopg2.extras import DictCursor
import os

def insert_mash(data):
    conn = get_connection(os.getenv('POSTGRES_DB'))
    sql = "INSERT INTO mashes(winner_name, loser_name, timestamp,remote_addr, uuid) VALUES (%s, %s, %s, %s, %s)"
    if data['winner'] == 'right':
        winner = data['rightid']
        loser = data['leftid']
    else:
        winner = data['leftid']
        loser = data['rightid']
    conn.cursor().execute(sql, (winner, loser, data['timestamp'], data['remote_addr'], data['uuid']))
    player_lock_sql = "SELECT name, score from players where name = %s or name = %s FOR UPDATE"
    curs = conn.cursor(cursor_factory=DictCursor)
    curs.execute(player_lock_sql, (winner, loser))
    player_scores = {}
    for row in curs.fetchall():
        player_scores[row['name']] = row['score']
    new_winner_score, new_loser_score = calc_rating(player_scores[winner], player_scores[loser])
    player_update_sql = "UPDATE players set score = %s where name = %s"
    conn.cursor().execute(player_update_sql, (new_winner_score, winner))
    conn.cursor().execute(player_update_sql, (new_loser_score, loser))
    conn.commit()

def get_ordered_players():
    conn = get_connection(os.getenv('POSTGRES_DB'))
    sql = "SELECT name from players order by score asc, random()"
    curs = conn.cursor(cursor_factory=DictCursor)
    curs.execute(sql)
    return [row['name'] for row in curs.fetchall()]
