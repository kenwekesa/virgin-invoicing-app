# Generated by Django 3.2.8 on 2022-01-13 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0018_alter_invoiceproduct_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceproduct',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
