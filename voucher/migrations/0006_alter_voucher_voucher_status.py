# Generated by Django 3.2.8 on 2022-01-05 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0005_voucher_voucher_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voucher',
            name='voucher_status',
            field=models.CharField(blank=True, choices=[('CANCELLED', 'CANCELLED'), ('EMAIL_SENT', 'EMAIL_SENT'), ('MODIFIED', 'MODIFIED')], default='NEW', max_length=19, null=True),
        ),
    ]
