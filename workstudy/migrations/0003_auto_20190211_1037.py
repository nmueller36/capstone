# Generated by Django 2.1.5 on 2019-02-11 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workstudy', '0002_auto_20190209_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalinfo',
            name='id',
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='first_name',
            field=models.CharField(max_length=256, primary_key=True, serialize=False),
        ),
    ]
