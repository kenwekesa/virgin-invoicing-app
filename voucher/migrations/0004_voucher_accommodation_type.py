# Generated by Django 3.2.8 on 2022-01-04 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0003_auto_20220103_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='accommodation_type',
            field=models.CharField(choices=[('RESIDENT', 'RESIDENT'), ('NON RESIDENT', 'NON RESIDENT')], default='RESIDENT', max_length=19),
        ),
    ]
