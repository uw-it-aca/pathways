# Generated by Django 3.2.7 on 2021-10-21 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0005_course_course_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='gpa_distro',
            field=models.JSONField(null=True),
        ),
    ]
