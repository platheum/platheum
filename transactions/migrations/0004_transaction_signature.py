# Generated by Django 4.0 on 2022-03-22 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_alter_transaction_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='signature',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
