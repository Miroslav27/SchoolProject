# Generated by Django 4.1.1 on 2022-10-06 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0008_course_dummy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='tag',
            new_name='tags',
        ),
    ]
