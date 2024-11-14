FROM python:3.8

WORKDIR /app

COPY ./app_user_management/requirement.txt /app/

RUN    python -m pip install --upgrade pip

RUN    pip install -r requirement.txt

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
