# Generated by Django 4.2.2 on 2023-08-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order', '0003_order_discount_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_discount',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]