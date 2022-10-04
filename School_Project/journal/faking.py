from journal.models import Student,Group,Teacher
import random
import faker

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

def add_fake_course():
    pass
def delete_all_fakes():
    Teacher.objects.filter(dummy=True).delete()
    Student.objects.filter(dummy=True).delete()
    print("Dummies been erased!")