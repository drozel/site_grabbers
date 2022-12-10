#!/bin/bash

cd "$(dirname "$BASH_SOURCE")"

python3 update.py &
PID_UPDATE="$!"

python3 manage.py runserver 0.0.0.0:80 &
PID_DJANGO="$!"

wait -n $PID_UPDATE $PID_DJANGO
