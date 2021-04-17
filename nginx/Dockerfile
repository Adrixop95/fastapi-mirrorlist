FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
COPY default.conf /etc/nginx/conf.d/default.conf
COPY favicon.ico /usr/share/nginx/html/favicon.ico

ADD statics.tar /usr/share/nginx/html/8/
