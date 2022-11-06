from django import template
import re

from journal.models import Course

register = template.Library()

@register.filter
def evennums(alphanum_list):
    return [x for x in alphanum_list if (str(x).isnumeric() and int(x)%2==0)]

@register.filter
def whyiwedoingthis(text):
    return text.replace("?","Dont ask!")

@register.filter
def wordscount(text):
    return len(re.findall(r'\b\w*[A-Za-z]\w*\b', text))

@register.inclusion_tag("includes/course_list.html")
def most_popular_courses():
    return {
        'object_list': Course.objects.all().select_related('teacher').prefetch_related('tags').exclude(teacher__isnull=True).order_by("-students_count")[:5]
    }