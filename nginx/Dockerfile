FROM nginx:latest
LABEL maintainer="wwt780406@gmail.com"
COPY nginx.conf /etc/nginx/nginx.conf
COPY big_data_interview_django-nginx.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/ && \
    ln -s /etc/nginx/sites-available/dashboard-nginx.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]