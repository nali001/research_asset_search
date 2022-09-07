FROM nginx:1.21.6
ENV HOME=/nginx_server
ENV APP_HOME=/nginx_server/search_engine_app

RUN mkdir $HOME $APP_HOME $APP_HOME/static

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d/

WORKDIR $APP_HOME
