from django import forms
from journal.models import Group,Student,CourseCategory, Tag,Teacher,Course
from django.core.validators import MinValueValidator

class StudentCreateForm(forms.Form):
    firstname = forms.CharField(required=True,)
    surname = forms.CharField(required=True, validators=[] )
    age = forms.IntegerField(min_value=18,validators=[MinValueValidator(18)])
    email = forms.CharField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all())

    def clean_firstname(self):
        firstname=self.cleaned_data["firstname"]
        if " " in firstname:
            raise forms.ValidationError(" Пробіли не допускаються,")
        return firstname

    def clean_surname(self):
        surname=self.cleaned_data["surname"]
        if " " in surname:
            raise forms.ValidationError(" Пробіли не допускаються,")
        if surname in Student.objects.all(surname=surname):
            raise forms.ValidationError(" Студент з таким призвіщем вже існує, спробуйте щось інше ")
        return surname

    def create_student(self):
        student = Student.objects.create(
            firstname=self.cleaned_data["firstname"],
            surname=self.cleaned_data["surname"],
            age=self.cleaned_data["age"],
            email=self.cleaned_data["email"],
            group=self.cleaned_data["group"],
        )
        return student

class CourseCreateForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    category = forms.ModelChoiceField(queryset=CourseCategory.objects.all(), required=True )
    description = forms.CharField()
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), required=True)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    def clean_name(self):
        name=self.cleaned_data["name"]
        if name in Course.objects.all(name=name):
            raise forms.ValidationError("Така назва курсу вже існує")
        return name
    def create_course(self):
        course = Course.objects.create(
            name=self.cleaned_data["name"],
            category=self.cleaned_data["category"],
            description=self.cleaned_data["description"],
            teacher=self.cleaned_data["teacher"],

        )
        course.tags.add(*self.cleaned_data['tags'])
        return course