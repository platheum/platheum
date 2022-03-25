# Generated by Django 4.0 on 2022-03-14 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.TextField()),
                ('amount', models.DecimalField(decimal_places=7, default=0.0, max_digits=12)),
                ('txType', models.IntegerField(choices=[[211, 'B2C'], [330, 'C2C']])),
                ('has_block', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[['pending', 'pending'], ['invalid', 'invalid'], ['authorized', 'authorized']], default='invalid', help_text='Specify the transaction stage', max_length=200)),
                ('sender', models.CharField(help_text='The user hash:id who sends the coins', max_length=200)),
                ('receiver', models.CharField(help_text='The wallet receive address who receive the funds', max_length=200)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False, help_text='shows if the transaction is completed')),
            ],
        ),
    ]