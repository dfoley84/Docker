FROM prom/cloudwatch-exporter:latest

ADD config.yml /config/
COPY setup.sh /setup.sh
RUN chmod +x /setup.sh

EXPOSE 9106

ENTRYPOINT ["/setup.sh"]
