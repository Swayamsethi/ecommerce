# Generated by Django 5.1.3 on 2024-11-21 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
