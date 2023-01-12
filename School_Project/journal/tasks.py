from django.contrib.auth import get_user_model

from School_Project.celery import app
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
import rest_framework


#from journal.models import Student


#celery -A School_Project worker -l INFO
#celery -A School_Project worker -P solo -l INFO
#celery -A School_Project beat
#py manage.py runserver


@app.task
def print_debug():
    print("Celery works")

@app.task
def send_single_mail(subject="No subject", message="Spam!", from_email="no_reply@mail.com", address=["bucket@mail.com",]):
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=address)

@app.task
def new_course_notification(course_name):
    from journal.models import Student

    for student in Student.objects.all():

        message = f"Dear {student.firstname} {student.surname}, there is a new course {course_name} available!"
        address = [student.email, ]
        subject = f"New Course {course_name} is now available!"
        from_email = f"no-reply-{course_name}@mail.com"
        send_single_mail.delay(subject=subject,message=message,from_email=from_email,address=address)

@app.task
def daily_courses_news():
    from journal.models import Course,Student
    from datetime import timedelta,datetime
    last_24h=datetime.now()-timedelta(days=1)
    from django.db.models import Q
    courses_list = ("\n").join(Course.objects.filter(Q(created_at__gte=last_24h)).values_list('name',flat=True))
    address_list = Student.objects.values_list('email', flat=True)
    if courses_list:
        subject = "New Courses!"
        from_email = f"no-reply@mail.com"
        message = f"Dear student, there is a list of new courses we setup last 24 h: {courses_list} "
        for email in address_list:
            address=[email,]
            send_single_mail.delay(subject=subject,message=message,from_email=from_email,address=address)
    else : pass

@app.task()
def count_course_stat():
    from journal.models import Course

    for course in Course.objects.all():
        course.students_count = course.student_set.all().count()
        course.save()

def create_student():
    pass

@app.task()
def issue_daily_token():
    for user in get_user_model().objects.all():
        user.auth_token.delete()
        token=Token.objects.get_or_create(user=user)
        send_single_mail(subject="Your new token for today",message=f"Token:{token} !", address=[user.email,])
        
