FROM mongo:7.0

ENV MONGO_INITDB_DATABASE=blog_db

COPY init/ /docker-entrypoint-initdb.d/

RUN chmod 755 /docker-entrypoint-initdb.d/*
