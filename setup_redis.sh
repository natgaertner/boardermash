#!/bin/bash

(redis-server &> /dev/null &)
source /var/www/postmash/bin/activate
echo 'butt'
(python /var/www/postmash/postmash/copy_to_redis.py)
echo 'butt2'
