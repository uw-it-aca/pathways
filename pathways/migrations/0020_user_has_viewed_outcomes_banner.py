# Generated by Django 3.2.16 on 2022-10-04 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0019_major_career_center_major'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_viewed_outcomes_banner',
            field=models.BooleanField(default=False),
        ),
    ]