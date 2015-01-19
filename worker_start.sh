#!/bin/bash
source $MASH_HOME"venv/bin/activate"
(python $ENV_ROOT"boardermash/log_record_stream_handler.py" &)
for i in `seq 1 5` ; do
    (python $ENV_ROOT"boardermash/worker.py" &)
done
