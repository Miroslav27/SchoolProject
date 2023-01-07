from journal.models import CourseCategory

def get_categories(request):
    return {
        "course_categories": CourseCategory.objects.all(),
        "alphanum_list":[1,2,3,4,5,6,"shs",7,8,10,"11"],

    }