# Generated by Django 2.1.5 on 2019-02-19 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workstudy', '0008_auto_20190215_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinfo',
            name='perferred_name',
            field=models.CharField(default='null', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='siteinfo',
            name='clearances_needed',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
