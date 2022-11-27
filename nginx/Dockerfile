FROM nginx:1.21.6
ENV HOME=/nginx_server
ENV APP_HOME=/nginx_server/search_engine_app

RUN mkdir $HOME $APP_HOME $APP_HOME/static

WORKDIR $APP_HOME
COPY ./static ./static


