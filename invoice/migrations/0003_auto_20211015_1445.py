# Generated by Django 3.2.8 on 2021-10-15 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_auto_20211014_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='title',
        ),
        migrations.AddField(
            model_name='invoice',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='quantity',
            field=models.CharField(default=1, max_length=200),
        ),
        migrations.AddField(
            model_name='invoice',
            name='unit_price',
            field=models.CharField(default=0, max_length=30),
        ),
    ]
