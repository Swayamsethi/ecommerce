# Generated by Django 5.1.3 on 2024-11-21 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_user_profile_pic_alter_products_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='stock',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
