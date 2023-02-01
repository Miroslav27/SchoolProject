from django.urls import path
from api import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"students",views.StudentsListView, basename="students")
router.register(r"teachers",views.TeachersListView, basename="teachers")
router.register(r"groups",views.GroupsListView, basename="groups")
router.register(r"auctions",views.AuctionListView, basename="auctions")
urlpatterns = [
    #path("students/", views.StudentsListView.as_view(), name="student_list"),
    #path("teachers/",views.TeachersListView.as_view(),name="teacher_list"),
    #path("groups/",views.GroupsListView.as_view(),name="group_list"),
]+router.urls