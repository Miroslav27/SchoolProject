import sys,random
from django.shortcuts import render
from django.http import HttpResponse,request
from django.views.generic import TemplateView,View,ListView,DetailView,FormView
from journal.models import Student, Group, Teacher, CourseCategory,Course, Tag

from journal.faking import add_fake_student,add_fake_teacher,delete_all_fakes,add_fake_course,add_fake_tags
from journal.forms import StudentCreateForm,CourseCreateForm
# Create your views here.

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


class StudentCreateView(TemplateView):
    template_name = "create_student.html"

    def get_context_data(self, **kwargs):
        context = super(StudentCreateView,self).get_context_data(**kwargs)
        context["form"] = StudentCreateForm()
        context['course_categories'] = CourseCategory.objects.all()
        return context
    def post(self,request):
        form= StudentCreateForm(data=request.POST)
        context = self.get_context_data()
        context["form"] = form
        if form.is_valid():
            form.create_student()
            context["success_mes"]="Студента успішно створено"
            context["form"] = StudentCreateForm()
        return self.render_to_response(context)

class CourseCreateView(TemplateView):
    template_name = "create_course.html"

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView,self).get_context_data(**kwargs)
        context["form"] = CourseCreateForm()
        context['course_categories'] = CourseCategory.objects.all()
        return context

    def post(self,request):
        form = CourseCreateForm(data=request.POST)
        context = self.get_context_data()
        context["form"] = form
        if form.is_valid():
            form.create_course()
            context["success_mes"]="Курс успішно створено"
            context["form"]= CourseCreateForm
        return self.render_to_response(context)

class CreateFakesView(IndexView):
    template_name = "create_fakes.html"
    faking_functions = {"student":add_fake_student,"teacher":add_fake_teacher,
                        "course":add_fake_course,"tag":add_fake_tags,"delete":delete_all_fakes
                       }

    def get_all_context(self):

        context_dict = {"students": Student.objects.all(), "teachers": Teacher.objects.all(),
                        "groups": Group.objects.all(), "courses": Course.objects.all(), "tags": Tag.objects.all()}
        context_dict['course_categories'] = CourseCategory.objects.all()
        return context_dict
    def get(self, request):

        return render(request, "create_fakes.html", context=self.get_all_context())
    def post(self,request):
        if self.faking_functions[self.request.POST["submit_button"]]:
            self.faking_functions[self.request.POST["submit_button"]](quantity=int(self.request.POST["number"]))
            print("+")

        return render(request, "create_fakes.html", context=self.get_all_context())

