# Do not build this directly. Use the script docker_build.sh

FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client netcat screen vim \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY backend/requirements.txt ./

RUN pip install -r requirements.txt

COPY deployment/uwsgi ./uwsgi
COPY backend .

COPY deployment/frontend_out/*.js src/static/frontend/dist
COPY deployment/frontend_out/index.html src/static/frontend/index.html

<<<<<<< HEAD
COPY deployment/frontend_out src/static/app/dist
RUN src/manage.py collectstatic -c --noinput
RUN src/manage.py makemigrations users
RUN src/manage.py makemigrations

EXPOSE 8000 7070
=======
RUN src/manage.py collectstatic -c --noinput \
 && src/manage.py makemigrations users \
 && src/manage.py makemigrations \
 && export PYTHONPATH=$PYTHONPATH:/code/src \
 && export DJANGO_SETTINGS_MODULE=streisand.settings.www_settings

EXPOSE 8000 7070
ENV PYTHONPATH /code/src
ENV DJANGO_SETTINGS_MODULE streisand.settings.www_settings

>>>>>>> origin/develop
CMD ["/usr/local/bin/uwsgi", "--emperor", "/code/uwsgi", "--die-on-term"]
