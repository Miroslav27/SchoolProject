import sys,random

from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,request
from django.urls import reverse_lazy
from django.views.generic import TemplateView,View,ListView,DetailView,FormView, CreateView, UpdateView
from journal.models import Student, Group, Teacher, CourseCategory,Course, Tag, Auction

from journal.faking import add_fake_student,add_fake_teacher,delete_all_fakes,add_fake_course,add_fake_tags
from journal.forms import StudentCreateForm, CourseCreateForm, AuctionLotForm

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Create your views here.


@ method_decorator(cache_page(60,key_prefix="index"),"get")
class IndexView(ListView):

    template_name = "index.html"
    model = Course
    paginate_by = 10

    def get_queryset(self):
        queryset = super(IndexView,self).get_queryset()

        return queryset.select_related('teacher').prefetch_related('tags').exclude(teacher__isnull=True).order_by("?")

@ method_decorator(cache_page(60,key_prefix="course_by_category"),"get")
class CourseByCategoryView(IndexView):

    def get_queryset(self):
        queryset = super(CourseByCategoryView, self).get_queryset()
        return queryset.select_related('teacher').prefetch_related('tags').filter(category__id=self.kwargs["category_id"])


class StudentCreateView(FormView):
    template_name = "create_student.html"
    form_class = StudentCreateForm
    success_url = reverse_lazy("student_create")

    def form_valid(self, form):
        form.save()
        return super(StudentCreateView, self).form_valid(StudentCreateForm())


class StudentEditView(UpdateView):
    template_name = "create_student.html"
    model = Student
    form_class = StudentCreateForm
    success_url = reverse_lazy("student_edit")
    pk_url_kwarg = "student_id"

    def get_success_url(self):
        return reverse_lazy("student_edit",args=(self.kwargs['student_id'],))

@ method_decorator(cache_page(60,key_prefix="students_by_course"),"get")
class StudentByCourseView(ListView):
    template_name = "students_by_course.html"
    model = Student
    paginate_by = 10

    def get_queryset(self):
        queryset = super(StudentByCourseView,self).get_queryset()
        return queryset.filter(course__id=self.kwargs["course_id"])


class CourseCreateView(CreateView):
    template_name = "create_course.html"
    model = Course
    form_class = CourseCreateForm
    success_url = reverse_lazy("course_create")


class CourseEditView(UpdateView):
    template_name = "create_course.html"
    form_class = CourseCreateForm
    model = Course
    pk_url_kwarg = "course_id"

    def get_success_url(self):
        return reverse_lazy("course_edit",args=(self.kwargs['course_id'],))


class AuctionLobbyView(CreateView):
    model = Auction
    template_name = "auction.html"
    form_class = AuctionLotForm
    success_url = reverse_lazy("auction")
    pk_url_kwarg = "lot_id"
    def get_success_url(self):
        return reverse_lazy("auction_lot", kwargs={'lot_id': self.object.pk})
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(AuctionLobbyView, self).form_valid(form)


class AuctionEditLobbyView(UpdateView):
    model = Auction
    template_name = "auction.html"
    form_class = AuctionLotForm



class AuctionLotView(DetailView):
    queryset = Auction.objects.all()
    model = Auction
    template_name = "auction_lot.html"
    form_class = AuctionLotForm

    def get_object(self):
        return self.queryset.filter(pk=self.kwargs["lot_id"])

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

