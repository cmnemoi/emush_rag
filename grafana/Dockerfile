FROM grafana/grafana-oss:12.1.0

COPY ./provisioning /etc/grafana/provisioning

EXPOSE 3000

CMD ["grafana-server", "web"]