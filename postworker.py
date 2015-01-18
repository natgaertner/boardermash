import boto.swf.layer2 as swf
from boto.swf.exceptions import SWFWorkflowExecutionAlreadyStartedError
import json
import logging
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler('/var/log/postmash/redisworker.log')
file_handler.setLevel(logging.INFO)
logger = logging.getLogger('redisworker')
logger.addHandler(file_handler)

def enqueue_work(jsondata):
    logger.warn('enqueuing work {data}'.format(data=jsondata))
    #some dumb retries for workflow ID clashes
    for _ in range(5):
	try:
	    swf.WorkflowType(name='PostMashWorkflow', domain='PostMashDomain',version='1.0', task_list='PostMashTasks').start(input=jsondata)
	    break
	except SWFWorkflowExecutionAlreadyStartedError:
	    logger.warn('had a workflow ID clash')
    logger.warn('work enqueued')
