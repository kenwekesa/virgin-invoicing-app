# Generated by Django 3.2.8 on 2021-10-29 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_auto_20211028_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='invoice',
            field=models.ManyToManyField(through='invoice.InvoiceProduct', to='invoice.Invoice'),
        ),
    ]
