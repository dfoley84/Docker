FROM ubuntu:18.04

RUN apt update -y && \
    apt install python3.3 python3-dev gcc libpng-dev g++ build-essential libssl-dev libffi-dev curl wget -y

RUN apt install python3-pip  libpython2.7-stdlib -y && \
    apt install python-pip -y && \
    pip3 install wheel && \
    pip3 install --upgrade setuptools

RUN apt-get update -y && \
    apt upgrade -y

RUN apt update && \
    apt install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*

RUN apt-add-repository ppa:ansible/ansible -y && \
    apt-get update -y && \
    apt install ansible -y

RUN pip3 install pyvmomi &&\
    pip3 install requests-credssp && \
    pip3 install pywinrm && \
    pip3 install pywinrm[credssp] && \
    pip install pyvmomi &&\
    pip install requests-credssp && \
    pip install pywinrm && \
    pip install pywinrm[credssp]

RUN mkdir -p ~/bin && \
    wget ./https://releases.hashicorp.com/terraform/0.12.24/terraform_0.12.24_linux_amd64.zip && \
    unzip ./terraform_0.12.24_linux_amd64.zip && \
    mv terraform ~/bin
    
RUN wget ./https://releases.hashicorp.com/packer/1.5.6/packer_1.5.6_linux_amd64.zip && \
    unzip ./packer_1.5.6_linux_amd64.zip && \
    mv packer ~/bin

RUN apt update && \
    apt upgarde -y && \
    apt install git -y && \
    apt install openssh-server -y && \
    sed -i 's|session required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd && \
    mkdir -p /var/run/sshd && \
    apt install openjdk-8-jdk -y && \
    apt install maven -y && \
    adduser --quiet jenkins && \
    echo "jenkins:jenkins" | chpasswd && \
    mkdir /home/jenkins/.m2

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
