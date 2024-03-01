set -eu
cd /var/app

source ./.venv/bin/activate

cd ./src

poetry run python main.py