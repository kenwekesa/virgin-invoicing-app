# Generated by Django 3.2.8 on 2021-12-30 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0016_auto_20211218_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='apply_discount',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='discount',
            field=models.CharField(blank=True, default=0, max_length=10, null=True),
        ),
    ]
