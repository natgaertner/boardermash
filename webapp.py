from flask import Flask, request, session, render_template
import json
import logging
import redis
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
import boto.sqs
from boto.sqs.message import Message
from uuid import uuid4
from mash_calc import select_pair
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
UUID_EX_SECONDS = 600
app = Flask("webapp")
app.config['SESSION_COOKIE_HTTPONLY'] = False
file_handler = RotatingFileHandler(os.getenv('FLASK_LOG'))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(name)-15s %(levelname)-8s %(message)s'))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('connecting to redis')
r = redis.StrictRedis(host='localhost', port=6379, db=0)
av_r = redis.StrictRedis(host='localhost', port=6379, db=1)
uuid_r = redis.StrictRedis(host='localhost',port=6379,db=2)
app.logger.info('connecting to sqs')
q = boto.sqs.connect_to_region('us-west-2').get_queue(os.getenv("SQS_QUEUE_NAME"))
app.secret_key = os.getenv('SESSION_SECRET')
app.logger.info('setup done')

@app.route('/')
def idx():
    return render_template('index.html')

@app.route('/twoboarders')
def twoboarders():
    ordered_players = json.loads(r.get('ordered_players'))
    idx1,idx2 = select_pair(ordered_players)
    player1 = ordered_players[idx1]
    player2 = ordered_players[idx2]
    app.logger.debug('leftkey: {player1} rightkey: {player2}'.format(player1=player1.encode('utf-8'), player2=player2.encode('utf-8')))
    session['rightkey'] = player2
    session['leftkey'] = player1
    uuid = uuid4().hex
    uuid_r.setex(uuid,UUID_EX_SECONDS,json.dumps({'leftkey':player1,'rightkey':player2}))
    session['uuid'] = uuid
    return json.dumps({'matchuuid':uuid,'leftboarder':{'boarder_name':player1, 'av':av_r.get(player1)},'rightboarder':{'boarder_name':player2, 'av':av_r.get(player2)}})

@app.route('/mash', methods=['POST'])
def mash():
    data = dict(request.json)
    data.update({"timestamp":datetime.now().strftime(TIME_FORMAT), "remote_addr":request.headers.get('X-Forwarded-For')})
    if not data.has_key('uuid'):
        data['uuid'] = session['uuid']
    try:
        jsondata = json.dumps(data)
        app.logger.debug('enqueuing work {data}'.format(data=jsondata))
        app.logger.debug('session_key_right: {session_rkey} session_key_left: {session_lkey}'.format(session_rkey=session['rightkey'].encode('utf-8'), session_lkey=session['leftkey'].encode('utf-8')))
        m = Message()
        m.set_body(jsondata)
        q.write(m)
    except Exception as e:
        app.logger.exception(e)
    return '0', 200

if __name__ == '__main__':
    app.run()
