"""
1. Написати АПІ для Груп, Студентів та Вчителів (CRUD)
2.Доступ до АПІ має бути лише у аутинтифікованих користувачів
3.Підключити Аутинтификацию через Токен
4. Генерувати новий токен що півночі
"""

from rest_framework import serializers
from journal.models import Student, Group, Course, Tag, Teacher



class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ("dummy",)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        exclude = ("dummy",)

class CourseSerializer(serializers.ModelSerializer):


    class Meta:
        model = Course
        exclude = ("dummy","created_at")

 #   tags = TagsSerializer(many=True)
  #  teacher = TeacherSerializer()

class StudentSerializer(serializers.ModelSerializer):

    #group_name = GroupSerializer(read_only=True,source="group")
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
   # course_list = CourseSerializer(read_only=True,many=True, source="course")
    course = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())
    class Meta:
        model = Student
        fields ="__all__"


    def create(self, validated_data):
        print(validated_data)
        course_data = validated_data.pop('course')
        student = super(StudentSerializer,self).create(validated_data)
        for course in course_data:
            student.course.add(course)
        return student