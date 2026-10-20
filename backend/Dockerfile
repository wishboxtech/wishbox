FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 libpq5 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements/all.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app app
COPY --chown=app:app manage.py ./
COPY --chown=app:app src ./src
COPY --chown=app:app settings ./settings
COPY --chown=app:app templates ./templates
COPY --chown=app:app openapi ./openapi
COPY --chown=app:app certs ./certs
COPY --chown=app:app tests ./tests
COPY --chown=app:app scripts ./scripts
COPY --chown=app:app docker/entrypoint.sh ./entrypoint.sh
RUN mkdir media static && chown app:app media static && chmod +x entrypoint.sh
USER app
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "src.core.wsgi:application"]
