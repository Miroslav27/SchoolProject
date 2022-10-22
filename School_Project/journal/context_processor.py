from journal.models import CourseCategory

def get_categories(request):
    return {
        "course_categories": CourseCategory.objects.all()
    }
