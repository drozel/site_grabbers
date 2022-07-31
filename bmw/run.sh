#!/bin/sh

trap "exit" INT TERM ERR
trap "kill 0" EXIT

python3 update.py &
python3 manage.py runserver &

wait
