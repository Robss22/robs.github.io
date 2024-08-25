# Generated by Django 5.0 on 2023-12-15 10:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0002_alter_student_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='former_school',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='scores',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='parents_contact',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Phone number must be between 10 and 20 digits.', regex='^\\d{10,20}$')]),
        ),
    ]
