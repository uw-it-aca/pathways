# Generated by Django 3.2.7 on 2021-09-20 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0002_auto_20210920_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='major',
            name='common_course_decl',
            field=models.JSONField(null=True),
        ),
    ]
