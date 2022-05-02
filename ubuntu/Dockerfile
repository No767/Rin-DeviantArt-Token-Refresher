# NOT WORKING...
FROM ubuntu:22.04
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3.10 python3.10-dev libffi-dev curl wget liblzma-dev 
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN sudo apt-get update && sudo apt-get install -y node.js 
RUN mkdir refresher
COPY requirements.txt ./refresher
COPY ./refresher/* ./refresher
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN pip install --upgrade -r /refresher/requirements.txt
RUN npm install pm2@latest -g
CMD ["pm2-runtime", "start", "refresher.config.js"]