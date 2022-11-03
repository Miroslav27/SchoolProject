from django.db import models
from django.core.validators import MinValueValidator, EmailValidator, RegexValidator

# Create your models here.

class Group(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} "


class Teacher(models.Model):
    firstname = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
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
    def __str__(self):
        return f"{self.name}: {self.category.name} ({self.teacher.surname})"
class Tag(models.Model):
    name = models.CharField(max_length=255)
    dummy = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name} "