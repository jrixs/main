FROM nginx:latest

RUN rm -f /etc/nginx/conf.d/default.conf
RUN rm -f /etc/nginx/nginx.conf

ADD nginx.conf /etc/nginx/

CMD nginx -g "daemon off;"
