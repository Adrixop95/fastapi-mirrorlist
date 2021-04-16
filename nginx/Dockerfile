FROM nginx:alpine as python-base

COPY index.html /usr/share/nginx/html/index.html
COPY default.conf /etc/nginx/conf.d/default.conf

ADD statics.tar /usr/share/nginx/html/public/latest