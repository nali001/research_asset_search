
FROM nginx:1.17-alpine


COPY ./nginx.conf /etc/nginx
COPY ./responses /usr/share/nginx/html/responses

CMD ["nginx", "-g", "daemon off;"]