# Generated by Django 4.1.1 on 2022-10-02 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0005_remove_teacher_group_group_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='teacher',
        ),
        migrations.AddField(
            model_name='teacher',
            name='groups',
            field=models.ManyToManyField(blank=True, to='journal.group'),
        ),
    ]