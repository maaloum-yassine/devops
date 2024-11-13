FROM python:3.8

WORKDIR /app

COPY requirement.txt .

RUN python -m pip install --upgrade pip &&  pip install -r requirement.txt 

COPY app_user_manafgement .

EXPOSE 8000

CMD ["python", "app_user_manafgement/manage.py", "runserver", "0.0.0.0:8000"]

