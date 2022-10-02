from django.shortcuts import render
from django.http import HttpResponse,request
from django.views.generic import TemplateView
from journal.models import Student, Group, Teacher

from journal.faking import add_fake_student,add_fake_teacher,delete_all_fakes
# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"
    def get_context(self):
        context_dict = {"students": Student.objects.all(), "teachers": Teacher.objects.all(),
                        "groups": Group.objects.all()}
        return context_dict

    def get(self,request):
        """
        Вивести всіх студентів
        Вивести всі группи
        Вивести всіх вчетелів
        Вивести всіх студентів для однієї групи
        Вивести всіх студентів для одного викладача
        Вивести усіх студентів чий вік більше 20
        Вивести усіх студентів для одного викладача чий вік більше 20
        Вивести усіх студентів у яких email на домені gmail.com
        :param request:
        :return:
        """
        return render(request,"index.html",context=self.get_context())


class CreateFakesView(IndexView):
    template_name = "create_fakes.html"

    def get(self, request):
        context_dict = {"students": Student.objects.all(), "teachers": Teacher.objects.all(),
                        "groups": Group.objects.all()}
        return render(request, "create_fakes.html", context=self.get_context())
    def post(self,request):

        return HttpResponse("post in fakes")


class FakeTeachersForm(CreateFakesView):
    def post(self,request):
        if self.request.POST["submit_button"] == "teacher":
            add_fake_teacher(int(self.request.POST["number"]))
        print(self.request.POST)
        return render(request, "create_fakes.html", context=self.get_context())



class FakeStudentsForm(CreateFakesView):
    def post(self, request):
        if self.request.POST["submit_button"]=="student":
            add_fake_student(int(self.request.POST["number"]))
        print(self.request.POST)
        return render(request, "create_fakes.html", context=self.get_context())

class DeleteDummiesForm(CreateFakesView):
    def post(self, request):
        if self.request.POST["submit_button"]=="delete":
            delete_all_fakes()
        return render(request, "create_fakes.html", context=self.get_context())
