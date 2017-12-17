FROM debian:latest
RUN apt-get update
RUN apt-get install nginx -y
RUN mkdir -p /var/www/media
RUN mkdir -p /var/www/static
ADD startup.sh /root/startup.sh
RUN chmod +x /root/startup.sh
ENTRYPOINT /bin/bash /root/startup.sh