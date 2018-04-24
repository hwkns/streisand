# Do not build this directly. Use the script docker_build.sh

FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client netcat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

COPY deployment/uwsgi.ini .
COPY backend .
COPY deployment/frontend_out src/static/app/dist
RUN src/manage.py collectstatic -c --noinput
RUN src/manage.py makemigrations users
RUN src/manage.py makemigrations
RUN src/manage.py migrate

EXPOSE 80
CMD ["/usr/local/bin/uwsgi", "--ini", "/code/uwsgi.ini", "--die-on-term"]
