FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install python3.3 python3-dev gcc libpng-dev g++ build-essential libssl-dev libffi-dev curl wget -y

RUN apt install python3-pip  libpython2.7-stdlib -y
RUN pip3 install wheel
RUN pip3 install --upgrade setuptools

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update -y 

RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y
RUN ACCEPT_EULA=Y apt-get install mssql-tools -y 
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile 
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
#RUN source ~/.bashrc

RUN apt-get install unixodbc-dev -y
RUN pip3 install --upgrade pyodbc
COPY ./requirements.txt /app/requirements.txt 

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app
ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
