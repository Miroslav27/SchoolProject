import sys,random
from django.shortcuts import render
from django.http import HttpResponse,request
from django.views.generic import TemplateView,View,ListView
from journal.models import Student, Group, Teacher, CourseCategory,Course, Tag

from journal.faking import add_fake_student,add_fake_teacher,delete_all_fakes,add_fake_course,add_fake_tags
# Create your views here.

""" 
class IndexView(TemplateView):
    template_name = "index.html"
    
    
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
        #self.get_print_context()
        return render(request,"index.html",context=self.get_context_data())
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context.update({
            'course_categories': CourseCategory.objects.all(),
            'courses': Course.objects.all().select_related('teacher').prefetch_related('tags') ,

        })
        return context
"""


class IndexView(ListView):
    template_name = "index.html"
    model = Course
    paginate_by = 10

    def get_queryset(self):
        queryset = super(IndexView,self).get_queryset()
        return queryset.select_related('teacher').prefetch_related('tags').exclude(teacher__isnull=True)

    def get_context_data(self, *args,  **kwargs):
        context = super(IndexView,self).get_context_data(*args,**kwargs)
        context['course_categories']=CourseCategory.objects.all()
        return context


class CreateFakesView(IndexView):
    template_name = "create_fakes.html"
    faking_functions = {"student":add_fake_student,"teacher":add_fake_teacher,
                        "course":add_fake_course,"tag":add_fake_tags,"delete":delete_all_fakes
                       }

    def get_all_context(self):
        context_dict = {"students": Student.objects.all(), "teachers": Teacher.objects.all(),
                        "groups": Group.objects.all(), "courses": Course.objects.all(), "tags": Tag.objects.all()}
        return context_dict
    def get(self, request):

        return render(request, "create_fakes.html", context=self.get_all_context())
    def post(self,request):
        if self.faking_functions[self.request.POST["submit_button"]]:
            self.faking_functions[self.request.POST["submit_button"]](quantity=int(self.request.POST["number"]))
            print("+")

        return render(request, "create_fakes.html", context=self.get_all_context())

