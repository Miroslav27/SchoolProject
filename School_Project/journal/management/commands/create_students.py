from django.core.management import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("students_ammount", nargs="+", type=int)

    def handle(self, *args, **options):
        import random, faker
        from journal.models import Student,Group,Course

        fake = faker.Faker()
        for i in range(sum(options["students_ammount"])):

            fullname = fake.name().split()
            fake_name, fake_surname = fullname[0], fullname[-1] # Unique Surname may Fail
            fake_email = f"{fake_name.lower().replace(' ', '.')}@{fake.domain_name()}"
            fake_age = random.randint(16, random.randint(16, 99))
            fake_group = random.choice(Group.objects.all())
            fake_student = Student(firstname=fake_name, surname=fake_surname, email=fake_email, age=fake_age,
                                       group=fake_group, dummy=True)

            fake_student.save()

            fake_student.course.add(random.choice(Course.objects.all()))
            fake_student.course.add(random.choice(Course.objects.all()))
