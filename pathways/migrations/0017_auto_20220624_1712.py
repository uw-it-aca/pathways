# Generated by Django 3.2.13 on 2022-06-25 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathways', '0016_alter_user_uwnetid'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_bottleneck',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='is_gateway',
            field=models.BooleanField(default=False),
        ),
    ]
