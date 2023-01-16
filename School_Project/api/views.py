from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.viewsets import ModelViewSet

from api.serializers import StudentSerializer, GroupSerializer, TeacherSerializer
from journal.models import Student, Group, Teacher


# Create your views here.
"""
class StudentsListView(APIView):

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class GroupListView(APIView):

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups,many=True)
        return Response(serializer.data)

class TeacherListView(APIView):

    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
"""

class StudentsListView(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)

   # queryset = Student.objects.none()
    def get_queryset(self):
        return Student.objects.all()


class TeachersListView(ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = (IsAuthenticated,)
   # queryset = Teacher.objects.none()
    def get_queryset(self):
        return Teacher.objects.all()


class GroupsListView(ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
   # queryset = Group.objects.none
    def get_queryset(self):
        return Group.objects.all()
