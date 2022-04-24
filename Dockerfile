FROM python:3.10.4-bullseye AS build_base
WORKDIR /server
COPY requirements.txt ./ /server/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# FROM keymetrics/pm2:16-buster AS deploy
# RUN npm install pm2 -g

CMD ["python", "./server/deviantart-token-refresher.py"]