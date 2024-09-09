FROM alpine:3.16
RUN apk add --no-cache bash curl jq unzip python3 py3-pip \
    && pip3 install awscli \
    && curl -fsSL "https://releases.hashicorp.com/packer/1.11.2/packer_1.11.2_linux_amd64.zip" -o packer.zip \
    && unzip packer.zip -d /usr/local/bin/ \
    && rm packer.zip
COPY pipe.sh /usr/local/bin/pipe.sh
RUN chmod +x /usr/local/bin/pipe.sh
ENTRYPOINT ["pipe.sh"]
