# pull official base image
FROM python:3.13.5

# create the appropriate directories
ENV APP_HOME=/usr/src/app

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y \
    libpq-dev \
    build-essential \
    curl \
    libcurl4-openssl-dev \
    python3-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libtiff-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    tcl-dev \
    tk-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libblas-dev \
    gfortran \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements/all.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r all.txt

RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR $APP_HOME

COPY ./build/entrypoint.sh $APP_HOME
RUN chmod +x $APP_HOME/entrypoint.sh

# copy project
COPY ./certs $APP_HOME/certs

COPY ./manage.py $APP_HOME
COPY ./templates $APP_HOME/templates
# COPY ./stream_scripts $APP_HOME/stream_scripts
# COPY ./locale $APP_HOME/locale
#RUN addgroup -S app && adduser -S app -G app
RUN chmod +x $APP_HOME/manage.py

# COPY ./locale $APP_HOME/locale
COPY ./src $APP_HOME/src
COPY ./settings $APP_HOME/settings
COPY ./templates $APP_HOME/templates
COPY ./openapi $APP_HOME/openapi
# chown all the files to the app user
RUN mkdir $APP_HOME/media $APP_HOME/static
RUN chown -R app:app $APP_HOME

RUN chmod +x $APP_HOME/manage.py
# RUN chmod +x $APP_HOME/stream_scripts/create_streams.py
# change to the app user
USER app

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
CMD [ "sh", "-c", "gunicorn -w 4 -b 0.0.0.0:8000 src.core.asgi:application -k src.core.worker.Worker" ]


# pull official base image
# FROM python:3.9.5

# # create the appropriate directories
# ENV APP_HOME=/usr/src/app

# # install psycopg2 dependencies
# RUN apt-get update \
#     && apt-get install -y \
#     libpq-dev \
#     build-essential \
#     curl \
#     libcurl4-openssl-dev \
#     python3-dev \
#     libffi-dev \
#     libjpeg-dev \
#     libpng-dev \
#     libfreetype6-dev \
#     liblcms2-dev \
#     libtiff-dev \
#     libopenjp2-7-dev \
#     libwebp-dev \
#     tcl-dev \
#     tk-dev \
#     libxml2-dev \
#     libxslt1-dev \
#     zlib1g-dev \
#     libblas-dev \
#     gfortran \
#     gcc \
#     g++ \
#     && rm -rf /var/lib/apt/lists/*

# COPY ./requirements/production.txt .
# RUN pip install --no-cache-dir -r production.txt

# RUN addgroup --system app && adduser --system --ingroup app app

# WORKDIR $APP_HOME

# COPY ./build/entrypoint.sh $APP_HOME
# RUN chmod +x $APP_HOME/entrypoint.sh

# # copy project
# COPY ./certs $APP_HOME/certs

# COPY ./manage.py $APP_HOME
# COPY ./templates $APP_HOME/templates
# # COPY ./stream_scripts $APP_HOME/stream_scripts
# # COPY ./locale $APP_HOME/locale
# #RUN addgroup -S app && adduser -S app -G app
# RUN chmod +x $APP_HOME/manage.py

# COPY ./locale $APP_HOME/locale
# COPY ./src $APP_HOME/src
# COPY ./settings $APP_HOME/settings
# COPY ./templates $APP_HOME/templates
# COPY ./openapi $APP_HOME/openapi
# # chown all the files to the app user
# RUN mkdir $APP_HOME/media $APP_HOME/static
# RUN chown -R app:app $APP_HOME

# RUN chmod +x $APP_HOME/manage.py
# # RUN chmod +x $APP_HOME/stream_scripts/create_streams.py
# # change to the app user
# USER app

# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
# CMD [ "sh", "-c", "gunicorn -w 4 -b 0.0.0.0 -p 8000  src.core.asgi:application -k src.core.worker.Worker" ]

