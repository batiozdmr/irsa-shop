FROM python:3.8.5

ARG AWS_CONTAINER_CREDENTIALS_RELATIVE_URI
# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    postgresql-client \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    gettext \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy in your requirements file
ADD requirements.txt /requirements.txt

# OR, if you're using a directory for your requirements, copy everything (comment out the above and uncomment this if so):
# ADD requirements /requirements

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir `grep -v 'python-magic-bin' /requirements.txt` \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir -p /opt/app
WORKDIR /opt/app
ADD . /opt/app

# uWSGI will listen on this port
EXPOSE 8000

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=shop.settings

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN python manage.py collectstatic --noinput && \
    chown -R ${APP_USER}:${APP_USER} /opt/app && \
    chown -R ${APP_USER}:${APP_USER} /usr/local/lib/python3.8/site-packages/translations && \
    chmod +x /opt/app/_deploymanifests/init.sh

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=shop/wsgi.py

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Start uWSGI
#CMD ["/usr/local/bin/gunicorn", "--workers=4", "shop.wsgi", "-b", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
