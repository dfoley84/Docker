FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt 
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]
