from flask import Flask, request, session, render_template
import json
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
app = Flask("webapp")
app.config['SESSION_COOKIE_HTTPONLY'] = False
file_handler = RotatingFileHandler(os.getenv('FLASK_LOG'))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(name)-15s %(levelname)-8s %(message)s'))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('connecting to redis')
app.logger.info('connecting to sqs')
app.logger.info('setup done')

@app.route('/')
def idx():
    return render_template('index-closed.html')

@app.route('/twoboarders2')
def done():
    return json.dumps({'leftboarder':{'boarder_name':"Thank you for participating in boardermash 2015"}, 'rightboarder':{'boarder_name':"mashing is now closed."}})

@app.route('/mash', methods=['POST'])
def mash():
    return 'boardermash over', 404

if __name__ == '__main__':
    app.run()
