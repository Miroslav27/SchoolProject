# Generated by Django 4.1.1 on 2022-10-02 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='dummy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teacher',
            name='dummy',
            field=models.BooleanField(default=False),
        ),
    ]