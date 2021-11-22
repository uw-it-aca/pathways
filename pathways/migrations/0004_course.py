# Generated by Django 3.2.7 on 2021-09-28 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0003_major_common_course_decl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('course_id', models.CharField(max_length=10)),
                ('course_title', models.CharField(max_length=120)),
            ],
        ),
    ]