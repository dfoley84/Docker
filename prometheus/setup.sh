#!/bin/bash
cat /tmp/prometheus.yml | sed -e "s#AWSREGION#$AWSREGION#g" | sed -e "s#ZONENAME#$ZONE#g" | sed -e "s#AWSROLE#$AWSROLE#" | sed -e "s#REMOTE#$REMOTE#g" >> /etc/prometheus/prometheus.yml
exec /bin/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/prometheus --web.console.libraries=/usr/share/prometheus/console_libraries --web.console.templates=/usr/share/prometheus/consoles



