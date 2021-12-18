# Generated by Django 3.2.8 on 2021-12-18 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0014_auto_20211125_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceproduct',
            name='prod_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceproduct',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.product'),
        ),
    ]
