# Generated by Django 4.0 on 2022-03-14 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='id',
        ),
        migrations.AddField(
            model_name='block',
            name='index',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
