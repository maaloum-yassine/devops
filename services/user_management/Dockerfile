FROM python:3.8

WORKDIR /app

COPY ./requirement.txt /app/

RUN    python -m pip install --upgrade pip

RUN    pip install -r requirement.txt

EXPOSE 8000

COPY ./tools/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["/app/entrypoint.sh"]