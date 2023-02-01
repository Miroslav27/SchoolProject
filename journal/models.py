from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, EmailValidator, RegexValidator
from journal.tasks import send_single_mail,new_course_notification
# Create your models here.

class Group(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} "


class Teacher(models.Model):
    firstname = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    age = models.PositiveSmallIntegerField()
    email = models.CharField(max_length=255)
    dummy = models.BooleanField(default=False)
    groups = models.ManyToManyField("journal.Group", blank=True )
    def __str__(self):
        return f"{self.title} {self.firstname} {self.surname} "

class Student(models.Model):
    firstname = models.CharField(max_length=255, validators=[RegexValidator(regex=r' ', inverse_match=True, message="Без пробілів!", code="Namespaces")])
    surname = models.CharField(max_length=255, unique=True,validators=[RegexValidator(regex=r' ', inverse_match=True, message="Без пробілів!", code="Namespaces")])
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18)])
    email = models.CharField(max_length=255, validators=[EmailValidator()], unique=True)
    group = models.ForeignKey("journal.Group", on_delete=models.SET_NULL, null=True)
    course = models.ManyToManyField("journal.Course", blank=True)
    dummy = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.firstname} {self.surname} {self.age} {self.group}"

class CourseCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} "
class Course(models.Model):
    name = models.CharField(max_length=255, unique=True,)
    category = models.ForeignKey("journal.CourseCategory",on_delete=models.SET_NULL,null=True)
    description = models.TextField()
    teacher = models.ForeignKey("journal.Teacher",on_delete=models.SET_NULL,null=True)
    tags = models.ManyToManyField("journal.Tag",blank=True)
    dummy = models.BooleanField(default=False)
    students_count = models.SmallIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.category.name} ({self.teacher.surname}) Students:{self.students_count}"

    def save(self, *args, **kwargs):
        # send email to the students (виникає циклічний імпорт якщо відсилати у тасках, тому запрос студентів виконую тут)
        if not self.pk:
            new_course_notification(self.name)

        super(Course, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    dummy = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name} "


class Currency(models.Model):
    created_at = models.DateTimeField()
    broker = models.CharField(max_length=255)
    usd_buy = models.DecimalField(decimal_places=2,max_digits=8)
    usd_sell = models.DecimalField(decimal_places=2,max_digits=8)
    eur_buy = models.DecimalField(decimal_places=2,max_digits=8)
    eur_sell = models.DecimalField(decimal_places=2,max_digits=8)

    def __str__(self):
        return f"{self.broker} : ({self.created_at})"

class Auction(models.Model):
    lot_name = models.CharField(max_length=32,unique=True)
    creator = models.ForeignKey(get_user_model(),related_name='%(class)s_creator' ,on_delete=models.SET_NULL, null=True)
    last_bid_value = models.DecimalField(decimal_places=2, max_digits=8, default=1, validators=[MinValueValidator(1)])
    bid_step_value = models.DecimalField(decimal_places=2, max_digits=8, default=1, validators=[MinValueValidator(0.01)])
    last_bid_user = models.ForeignKey(get_user_model(),related_name='%(class)s_bidder', on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.lot_name} : {self.last_bid_value} "

