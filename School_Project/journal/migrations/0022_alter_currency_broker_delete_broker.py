# Generated by Django 4.1.1 on 2023-01-12 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0021_broker_alter_currency_broker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='broker',
            field=models.CharField(default='Unknown', max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Broker',
        ),
    ]
