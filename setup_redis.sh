#!/bin/bash

(redis-server &> /dev/null &)
source $MASH_HOME"/venv/bin/activate"
(python $ENV_ROOT"boardermash/copy_to_redis.py")
