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
app = Flask("webapp")
app.config['SESSION_COOKIE_HTTPONLY'] = False
file_handler = RotatingFileHandler(os.getenv('FLASK_LOG'))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(name)-15s %(levelname)-8s %(message)s'))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('connecting to redis')
r = redis.StrictRedis(host='localhost', port=6379, db=0)
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
    session['rightkey'] = player2
    session['leftkey'] = player1
    return json.dumps({'leftboarder':{'boarder_name':player1},'rightboarder':{'boarder_name':player2}})

@app.route('/mash', methods=['POST'])
def mash():
    data = dict(request.json)
    data.update({"timestamp":datetime.now().strftime(TIME_FORMAT), "remote_addr":request.remote_addr, "uuid":uuid4().hex})
    if data['rightid'] != session['rightkey'] or data['leftid'] != session['leftkey']:
        app.logger.error('session and data keys mismatch. session keys: {rightkey}, {leftkey} data keys: {rightid}, {leftid}'.format(rightkey=session['rightkey'], leftkey=session['leftkey'], rightid = data['rightid'], leftid=data['leftid']))
        return 'a wild haxor appears', 500
    try:
        jsondata = json.dumps(data)
        app.logger.info('enqueuing work {data}'.format(data=jsondata))
        m = Message()
        m.set_body(jsondata)
        q.write(m)
    except Exception as e:
        app.logger.exception(e)
    return '0', 200

if __name__ == '__main__':
    app.run()
