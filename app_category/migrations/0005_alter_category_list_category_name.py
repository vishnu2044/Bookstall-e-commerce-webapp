# Generated by Django 4.2.2 on 2023-07-05 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_category', '0004_alter_category_list_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category_list',
            name='category_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]