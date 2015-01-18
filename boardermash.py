from flask import Flask, request, session, render_template
import json
import logging
import redis
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
import boto.sqs
from boto.sqs.message import Message
from mash_experiment import select_close_pair, select_random_pair
import random
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
MUTATION_CHANCE = .2
app = Flask(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False
#rsessions = redis.StrictRedis(host='localhost', port=6379, db=1)
#app.session_interface = RedisSessionInterface(rsessions)
#file_handler = RotatingFileHandler('/var/log/boardermash/application.log')
file_handler = RotatingFileHandler('application.log')
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
q = boto.sqs.connect_to_region('us-west-2').get_queue('boardermashes')
#app.secret_key = os.getenv('SESSION_SECRET')

@app.route('/')
def idx():
    return render_template('index.html')

@app.route('/twoboarders')
def twoboarders():
    ordered_players = json.loads(r.get('ordered_players'))
    if random.random() < MUTATION_CHANCE:
        idx1,idx2 = select_random_pair(range(len(ordered_players)))
    else:
        idx1,idx2 = select_close_pair(range(len(ordered_players)), 20)
    player1 = ordered_players[idx1]
    player2 = ordered_players[idx2]
    return json.dumps({'leftboarder':{'boarder_name':player1},'rightboarder':{'boarder_name':player2}})

@app.route('/mash', methods=['POST'])
def mash():
    data = dict(request.json)
    #data.update({"timestamp":datetime.now().strftime(TIME_FORMAT), "remote_addr":request.remote_addr, "rightid":session['rightkey'],"leftid":session['leftkey']})
    data.update({"timestamp":datetime.now().strftime(TIME_FORMAT), "remote_addr":request.remote_addr})
    try:
        jsondata = json.dumps(data)
        app.logger.warn('enqueuing work {data}'.format(data=jsondata))
        m = Message()
        m.set_body(jsondata)
        q.write(m)
        app.logger.warn('work enqueued')
    except Exception as e:
        app.logger.exception(e)
    return '0', 200

if __name__ == '__main__':
    app.run()
