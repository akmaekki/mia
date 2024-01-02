FROM python:3.12

COPY . /app

WORKDIR /app
RUN pip install pip --upgrade
RUN pip install -r requirements.txt
RUN pip install pyopenssl --upgrade

EXPOSE 5000

CMD [ "nameko", "run", "--config", "config.yml", "app" ]
