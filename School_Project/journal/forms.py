from django import forms
from journal.models import Group,Student,CourseCategory, Tag,Teacher,Course
from django.core.validators import MinValueValidator

class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = {"dummy"}

class CourseCreateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects,widget=forms.CheckboxSelectMultiple(),required=False)

    class Meta:
        model = Course
        exclude = {"dummy"}

