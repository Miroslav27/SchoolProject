import sys,random
from django.shortcuts import render
from django.http import HttpResponse,request
from django.views.generic import TemplateView,View,ListView,DetailView,FormView, CreateView
from journal.models import Student, Group, Teacher, CourseCategory,Course, Tag

from journal.faking import add_fake_student,add_fake_teacher,delete_all_fakes,add_fake_course,add_fake_tags
from journal.forms import StudentCreateForm, CourseCreateForm
# Create your views here.

class IndexView(ListView):
    template_name = "index.html"
    model = Course
    paginate_by = 10

    def get_queryset(self):
        queryset = super(IndexView,self).get_queryset()
        return queryset.select_related('teacher').prefetch_related('tags').exclude(teacher__isnull=True)


class StudentCreateView(FormView):
    template_name = "create_student.html"
    form_class = StudentCreateForm
    success_url = "/create_student"

    def form_valid(self, form):
        form.save()
        return super(StudentCreateView, self).form_valid(StudentCreateForm())


class CourseCreateView(CreateView):
    template_name = "create_course.html"
    model = Course
    form_class = CourseCreateForm
    success_url = "/create_course"


class CreateFakesView(IndexView):
    template_name = "create_fakes.html"
    faking_functions = {"student":add_fake_student,"teacher":add_fake_teacher,
                        "course":add_fake_course,"tag":add_fake_tags,"delete":delete_all_fakes
                       }

    def get_all_context(self):

        context_dict = {"students": Student.objects.count(), "teachers": Teacher.objects.count(),
                        "groups": Group.objects.count(), "courses": Course.objects.count(), "tags": Tag.objects.count()}
        context_dict['course_categories'] = CourseCategory.objects.all()
        return context_dict

    def get(self, request):

        return render(request, "create_fakes.html", context=self.get_all_context())
    def post(self,request):
        if self.faking_functions[self.request.POST["submit_button"]]:
            self.faking_functions[self.request.POST["submit_button"]](quantity=int(self.request.POST["number"]))
            print("+")

        return render(request, "create_fakes.html", context=self.get_all_context())

