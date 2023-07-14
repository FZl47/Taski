FROM python:3.10-slim


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SUPERUSER_USERNAME fzl
ENV DJANGP_SUPERUSER_EMAIL fzl@gmail.com
ENV DJANGP_SUPERUSER_PASSWORD Fazel



RUN mkdir app
WORKDIR /app

ADD ./requirements.txt /app

#RUN apt update -y
#RUN apt install gcc python3-dev musl-dev mariadb-dev -y

RUN pip install -r requirements.txt
RUN pip install cryptography
RUN pip install gunicorn 
RUN python3 -m pip install PyMySQL[rsa]
#RUN apt uninstall gcc python3-dev musl-dev

 
    #while ! python manage.py sqlflush ; do sleep 1; done && \
CMD python manage.py makemigrations --noinput && \
    while ! python manage.py migrate --noinput ; do sleep 1; done && \
   # python manage.py collectstatic --noinput && \
    python manage.py init-admin && \
    nohup python manage.py qcluster & \
    gunicorn -b 0.0.0.0:8000 config.wsgi && \
    python manage.py init-task   
