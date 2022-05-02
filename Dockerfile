FROM archlinux:latest
RUN pacman -Syu --noconfirm
RUN pacman -S python libffi nodejs-lts-gallium npm wget --noconfirm
RUN mkdir refresher
COPY requirements.txt ./refresher
COPY refresher.config.js ./refresher
COPY ./refresher/* ./refresher
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN pip install --upgrade -r /refresher/requirements.txt
RUN npm install pm2@latest -g
ARG PM2_PUBLIC_KEY_INGEST
ARG PM2_SECRET_KEY_INGEST
ENV PM2_PUBLIC_KEY=${PM2_PUBLIC_KEY_INGEST}
ENV PM2_SECRET_KEY=${PM2_SECRET_KEY_INGEST}
CMD ["pm2-runtime", "start", "./refresher/refresher.config.js"]
