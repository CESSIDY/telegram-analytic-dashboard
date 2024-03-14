set -eux
cd /var/app

source ./.venv/bin/activate

cd ./src
ls
poetry run honcho start
#poetry run gunicorn --bind 0.0.0.0:8051 'main:server'

#poetry run gunicorn --bind 127.0.0.1:8051 main:server
#poetry run python main.py
#poetry run uvicorn src.main:app --host 0.0.0.0 --port 8051 --reload

