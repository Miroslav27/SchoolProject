from journal.models import Student,Group,Teacher,Course,CourseCategory,Tag
import random
import faker
from lorem_text import lorem
def add_fake_student(quantity = 1):
    fake=faker.Faker()
    for i in range(quantity):
        fake_name = fake.name()
        fake_email = f"{fake_name.lower().replace(' ','.')}@{fake.domain_name()}"
        fake_age = random.randint(16, random.randint(16, 99))
        fake_group = random.choice(Group.objects.all())
        fake_student=Student(name=fake_name, email=fake_email, age=fake_age, group=fake_group, dummy=True)
        fake_student.save()
        print(f"fake {i+1} is ready!")

def add_fake_teacher(quantity = 1):
    fake=faker.Faker()
    rank=["Doc.","Proff","Sir",]
    for i in range(quantity):
        fake_name = f"{random.choice(rank)} {fake.name()}"
        fake_email = f" {fake_name.lower().replace(' ','.')}@{fake.domain_name()}"
        fake_age = random.randint(random.randint(16, 99), 99)
        fake_group = random.choice(Group.objects.all())
        fake_teacher=Teacher(name=fake_name, email=fake_email, age=fake_age, dummy=True)
        fake_teacher.save()
        fake_teacher.groups.set([fake_group.id])

        print(f"fake {i+1} is ready!")

def add_fake_course(quantity = 1):
    for _ in range(quantity):
        fake_desc = lorem.paragraphs(2)
        fake_name = lorem.words(3).capitalize()

        fake_course = Course(name=fake_name,category=random.choice(CourseCategory.objects.all()),
                             description=fake_desc,teacher=random.choice(Teacher.objects.all()),
                             dummy=True
                             )
        fake_course.save()
        fake_course.tags.add(random.choice(Tag.objects.all()))
        #fake_course.tags.set(fake_tag)
        print(f"fake {_ + 1} is ready!")

def add_fake_tags(quantity = 1):
    for _ in range(quantity):
        fake_tag = lorem.words(1)
        #fake_tag = random.choice(Tag.objects.all())
        fake_tag = Tag(name=fake_tag,dummy=True)
        fake_tag.save()
        #fake_course.tags.set(fake_tag)
def delete_all_fakes(quantity = 0):
    Teacher.objects.filter(dummy=True).delete()
    Student.objects.filter(dummy=True).delete()
    Course.objects.filter(dummy=True).delete()
    Tag.objects.filter(dummy=True).delete()
    print("Dummies been erased!")