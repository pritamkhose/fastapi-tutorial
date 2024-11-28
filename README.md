python3 -m venv .venv

source .venv/bin/activate

pip3 install fastapi uvicorn

uvicorn main:app

pip3 freeze > requirements.txt

pip3 install -r requirements.txt

pip3 install "fastapi[standard]"

fastapi run main.py

fastapi dev

https://www.youtube.com/watch?v=ED6PRjmXgBA

docker build -t fastapi-tutorial .

docker run --rm -it -p 8000:8000 fastapi-tutorial bash

ls -a

Cntl + D # exit cmd

docker rmi fastapi-tutorial

docker ps -a

docker images -a

docker compose up --build