# Generated by Django 4.0 on 2022-03-16 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[['100', 'pending'], ['200', 'invalid'], ['300', 'authorized']], default='invalid', help_text='Specify the transaction stage', max_length=200),
        ),
    ]
