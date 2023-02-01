from django.core.management import BaseCommand
import random

from lorem_text import lorem
from journal.models import Teacher,CourseCategory,Course,Tag

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("courses_ammount", nargs="+", type=int)

    def handle(self, *args, **options):
        for i in range(sum(options["courses_ammount"])):
            fake_desc = lorem.paragraphs(2)
            fake_name = lorem.words(3).capitalize()

            fake_course = Course(name=fake_name, category=random.choice(CourseCategory.objects.all()),
                                 description=fake_desc, teacher=random.choice(Teacher.objects.all()),
                                 dummy=True
                                 )
            fake_course.save()
            fake_course.tags.add(random.choice(Tag.objects.all()))