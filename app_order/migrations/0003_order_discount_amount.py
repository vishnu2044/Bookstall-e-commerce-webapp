# Generated by Django 4.2.2 on 2023-08-03 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0002_alter_orderitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount_amount',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
