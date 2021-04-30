FROM ubuntu:18.04

RUN apt update -y && \
    apt install python3.3 python3-dev gcc libpng-dev g++ build-essential libssl-dev libffi-dev curl wget unzip nano -y

RUN apt install python3-pip libpython2.7-stdlib install python-pip -y && \
    pip3 install wheel && \
    pip3 install --upgrade setuptools

RUN apt update && \
    apt install software-properties-common -y && \
    apt-add-repository --yes --update ppa:ansible/ansible && \
    apt install ansible -y 

RUN apt update && \
    apt install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && \
    apt install git openssh-server -y && \
    sed -i 's|session required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd && \
    mkdir -p /var/run/sshd

RUN apt install openjdk-8-jdk maven -y && \
    adduser --quiet jenkins && \
    echo "jenkins:jenkins" | chpasswd && \
    mkdir /home/jenkins/.m2

RUN pip3 install --upgrade pyvmomi && \
    pip install --upgrade pyvmomi
    
RUN pip3 install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git
RUN ansible-galaxy collection install community.vmware
RUN ansible-galaxy collection install community.windows

RUN service ssh start
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
