# Generated by Django 3.1.7 on 2021-05-14 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnerApp', '0006_test_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='end_time',
            field=models.DateTimeField(help_text='yyyy-mm-dd hh:mm'),
        ),
        migrations.AlterField(
            model_name='test',
            name='start_time',
            field=models.DateTimeField(help_text='yyyy-mm-dd hh:mm'),
        ),
    ]