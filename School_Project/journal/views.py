import sys,random
from django.shortcuts import render
from django.http import HttpResponse,request
from django.views.generic import TemplateView,View
from journal.models import Student, Group, Teacher, CourseCategory,Course

from journal.faking import add_fake_student,add_fake_teacher,delete_all_fakes,add_fake_course
# Create your views here.
"""
Зробити список курсів. Бажано використовувати bootstrap4 але не обов'язково.
Має бути наступний функціонал:
Меню категорій для курсів
Список курсів з пагінацією, по 10 курсів на сторінку
Картка курсу має мати: Назву, Опис, Ім'я викладача, короткий перелік тезісів курсу.
Запити до ДБ мають бути оптимізовані, максимально! Курси без викладача мають бути виключені із переліку.
"""





class SomeView(View):
    template_name = "index.html"
    print("it worked")

    def get(request):
        return HttpResponse()

class IndexView(TemplateView):
    template_name = "index.html"
    def get_all_context(self):
        context_dict = {"students": Student.objects.all(), "teachers": Teacher.objects.all(),
                        "groups": Group.objects.all(), "courses": Course.objects.all()}
        return context_dict
    def get_print_context(self):
        context_dict={}

        print("1.Вивести всіх студентів")
        print(Student.objects.all())
        print("2.Вивести всі группи")
        print(Group.objects.all())
        print("3.Вивести всіх вчетелів")
        print(Teacher.objects.all())
        print("4.Вивести всіх студентів для однієї групи")
        print(Student.objects.filter(group=random.choice(Group.objects.all())))
        print("5.Вивести всіх студентів для одного викладача")
        print(Student.objects.filter(group__teacher__id=random.choice(Teacher.objects.all()).id))
        print("6.Вивести усіх студентів чий вік більше 20")
        print(Student.objects.filter(age__gt=20))
        print("7.Вивести усіх студентів для одного викладача чий вік більше 20")
        print(Student.objects.filter(group__teacher__id=random.choice(Teacher.objects.all()).id).filter(age__gt=20))
        print("8.Вивести усіх студентів у яких email на домені gmail.com")
        print(Student.objects.filter(email__icontains="gmail.com"))
        return {"file":""}
    def get(self,request):
        self.get_print_context()
        return render(request,"index.html",context=self.get_context_data())
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context.update({
            'course_categories':CourseCategory.objects.all(),
            'courses':Course.objects.all(),

        })
        return context

class CreateFakesView(IndexView):
    template_name = "create_fakes.html"

    def get(self, request):
        context_dict = {"students": Student.objects.all(), "teachers": Teacher.objects.all(),
                        "groups": Group.objects.all(), 'courses':Course.objects.all,
                        'coursescategory':CourseCategory,
                        }
        return render(request, "create_fakes.html", context=self.get_all_context())
    def post(self,request):

        return HttpResponse("post in fakes")


class FakeTeachersForm(CreateFakesView):
    def post(self,request):
        if self.request.POST["submit_button"] == "teacher":
            add_fake_teacher(int(self.request.POST["number"]))
        print(self.request.POST)
        return render(request, "create_fakes.html", context=self.get_all_context())



class FakeStudentsForm(CreateFakesView):
    def post(self, request):
        if self.request.POST["submit_button"]=="student":
            add_fake_student(int(self.request.POST["number"]))
        print(self.request.POST)
        return render(request, "create_fakes.html", context=self.get_all_context())

class FakeCourseForm(CreateFakesView):
    def post(self, request):
        if self.request.POST["submit_button"]=="course":
            add_fake_course(int(self.request.POST["number"]))
        print(self.request.POST)
        return render(request, "create_fakes.html", context=self.get_all_context())
class DeleteDummiesForm(CreateFakesView):
    def post(self, request):
        if self.request.POST["submit_button"]=="delete":
            delete_all_fakes()
        return render(request, "create_fakes.html", context=self.get_all_context())
