# Generated by Django 4.1.1 on 2023-01-10 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0017_course_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('broker', models.CharField(max_length=255, unique=True)),
                ('usd_buy', models.DecimalField(decimal_places=2, max_digits=8)),
                ('usd_sell', models.DecimalField(decimal_places=2, max_digits=8)),
                ('eur_buy', models.DecimalField(decimal_places=2, max_digits=8)),
                ('eur_sell', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.AlterField(
            model_name='teacher',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
