# Generated by Django 3.2.18 on 2023-02-16 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0023_course_department_abbrev'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_viewed_coi_banner',
            field=models.BooleanField(default=False),
        ),
    ]
