# Generated by Django 3.2.8 on 2021-12-18 05:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0015_auto_20211218_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.product'),
        ),
        migrations.AlterField(
            model_name='invoiceproduct',
            name='quantity',
            field=models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
