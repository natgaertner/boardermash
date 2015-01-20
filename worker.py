import boto.sqs
import json
import os
import logging, logging.handlers
from db_tasks import insert_mash, get_ordered_players
from get_redis_connections import get_redis_connections
from psycopg2 import IntegrityError
import traceback

NUM_MESSAGES_TO_GET = 10

rootLogger = logging.getLogger(os.getenv('APPLICATION_NAME'))
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
rootLogger.addHandler(socketHandler)
logger = logging.getLogger(os.getenv('APPLICATION_NAME')+'.worker')
redis_connections = get_redis_connections()

q = boto.sqs.connect_to_region('us-west-2').get_queue(os.getenv('SQS_QUEUE_NAME'))

class BoarderMashWorker():
    def run(self):
        messages = []
        try:
            messages = q.get_messages(NUM_MESSAGES_TO_GET)
        except Exception as e:
            logger.error('exception polling sqs' + traceback.format_exc())
            return
        for message in messages:
            try:
                data = json.loads(message.get_body())
            except Exception as e:
                logger.warn('badly formed message ' + traceback.format_exc())
                return
            try:
                insert_mash(data)
                logger.info('inserted {data}'.format(data=json.dumps(data)))
                ordered_players = get_ordered_players()
                for r in redis_connections:
                    r.set('ordered_players', json.dumps(ordered_players))
                logger.info('updated players in redis hosts')
            except IntegrityError:
                #if it's a unique constraint violation we don't care
                pass
            except Exception as e:
                logger.error('exception inserting ' + traceback.format_exc())
                logger.info('data: {data}'.format(data=json.dumps(data)))
                return
            try:
                q.delete_message(message)
            except Exception as e:
                logger.error("couldn't delete " + traceback.format_exc())

if __name__ == '__main__':
    logger.info('starting worker')
    while True: BoarderMashWorker().run()
