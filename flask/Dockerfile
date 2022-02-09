FROM python:3.8

WORKDIR /app

COPY ./requirments.txt /app/requirments.txt 
RUN pip3 install -r requirments.txt

COPY . /app

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]
