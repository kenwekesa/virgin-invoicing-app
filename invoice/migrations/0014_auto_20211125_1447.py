# Generated by Django 3.2.8 on 2021-11-25 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0013_invoice_istaxable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='city',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='city',
        ),
        migrations.AddField(
            model_name='invoiceproduct',
            name='prod_description',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(default='Anonimous', max_length=200),
        ),
    ]
