#Building Docker Image based on the jnlp-salve to be used for FreeStyle Projects with Jenkins kubernetes plugin
#This Image will be used for Ansible jobs. 

FROM jenkins/jnlp-slave

RUN apt update -y && \
    apt install python3.3 python3-dev gcc libpng-dev g++ build-essential libssl-dev libffi-dev curl wget unzip nano -y

RUN apt install python3-pip libpython2.7-stdlib python-pip -y && \
    pip3 install wheel && \
    pip3 install --upgrade setuptools

RUN apt update && \
    apt install software-properties-common -y && \
    apt-add-repository --yes --update ppa:ansible/ansible && \
    apt install ansible -y 

RUN apt update && \
    apt install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pyvmomi && \
    pip install --upgrade pyvmomi
    
