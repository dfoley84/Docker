FROM microsoft/powershell:ubuntu16.04

RUN apt update -y && \
    apt install python3.3 python3-dev gcc libpng-dev g++ build-essential libssl-dev libffi-dev curl wget unzip -y

RUN apt install python3-pip  libpython2.7-stdlib -y && \
    apt install python-pip -y && \
    pip3 install wheel && \
    pip3 install --upgrade setuptools

RUN apt-get update -y && \
    apt upgrade -y

RUN apt update && \
    apt install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && \
    apt install git openssh-server -y && \
    sed -i 's|session required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd && \
    mkdir -p /var/run/sshd

RUN apt-get install -y --no-install-recommends libgdiplus libc6-dev

RUN apt install openjdk-8-jdk maven -y && \
    adduser --quiet jenkins && \
    echo "jenkins:jenkins" | chpasswd && \
    mkdir /home/jenkins/.m2
    
WORKDIR /root

SHELL [ "pwsh", "-command" ]
RUN Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
RUN Install-Module VMware.PowerCLI, SqlServer, ImportExcel -Scope AllUsers

SHELL [ "bash", "-c"]

RUN curl -o ./PowerCLI-Example-Scripts.zip -J -L https://github.com/vmware/PowerCLI-Example-Scripts/archive/master.zip && \
    unzip PowerCLI-Example-Scripts.zip && \
    rm -f PowerCLI-Example-Scripts.zip && \
    mv ./PowerCLI-Example-Scripts-master ./PowerCLI-Example-Scripts && \
    mv ./PowerCLI-Example-Scripts/Modules/* /root/.local/share/powershell/Modules/


RUN service ssh start
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
