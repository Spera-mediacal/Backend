FROM mysql:latest
COPY init.sql /docker-entrypoint-initdb.d/
EXPOSE 3306