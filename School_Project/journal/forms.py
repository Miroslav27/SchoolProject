from django import forms
from django.contrib.auth.models import User

from journal.models import Group,Student,CourseCategory, Tag,Teacher,Course
from django.core.validators import MinValueValidator

from journal.tasks import new_course_notification,send_single_mail


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = {"dummy"}


class CourseCreateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects,widget=forms.CheckboxSelectMultiple(),required=False)

    def send_notification(self):
        new_course_notification.delay(self.cleaned_data["name"])

    class Meta:
        model = Course
        exclude = {"dummy"}

