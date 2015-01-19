#!/bin/bash

(redis-server &> /dev/null &)
source /home/gaertner/code/boardermash/venv/bin/activate
(python $ENV_ROOT"copy_to_redis.py")
