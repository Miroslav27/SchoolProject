FROM python:3.11.0-buster
ENV PYTHONUNBUFFERED = 1
RUN mkdir /app
WORKDIR /app
COPY . .
RUN apt update && pip install mysqlclient #dontask
RUN pip install --upgrade pip && pip install -r requirements.txt

#CMD python manage.py runserver  0.0.0.0:8000


#docker build -t journal . fdgvdf
# docker run  -p 8000:8000  --name=journal -v C:\Users\Miroslav\PycharmProjects\Homework4.Django\School_Project:/app journal
# docker exec -it journal python manage.py makemigrations