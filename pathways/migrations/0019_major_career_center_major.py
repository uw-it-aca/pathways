# Generated by Django 3.2.15 on 2022-09-19 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0018_user_has_viewed_bottleneck_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='major',
            name='career_center_major',
            field=models.TextField(null=True),
        ),
    ]
