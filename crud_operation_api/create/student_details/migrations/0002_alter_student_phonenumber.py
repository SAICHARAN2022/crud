# Generated by Django 3.2.18 on 2023-04-18 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_details', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phonenumber',
            field=models.BigIntegerField(),
        ),
    ]
