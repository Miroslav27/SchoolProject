from django.db import models


"""Написати наступні моделі:
Teacher:
name
age
email

Group:
name

Student:
name
age
email"""
# Create your models here.

class Group(models.Model):

    name = models.CharField(max_length=255)
    #teacher = models.ManyToManyField("journal.Teacher")
    def __str__(self):
        return f"{self.name} "


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    email = models.CharField(max_length=255)
    dummy = models.BooleanField(default=False)
    groups = models.ManyToManyField("journal.Group", blank=True )
    def __str__(self):
        return f"{self.name} {self.age} "

class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    email = models.CharField(max_length=255)
    group = models.ForeignKey("journal.Group", on_delete=models.SET_NULL, null=True)
    dummy = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name} {self.age} {self.group}"