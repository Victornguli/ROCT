# Generated by Django 2.2.3 on 2019-07-31 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20190731_0858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oversightreport',
            old_name='report_name',
            new_name='oversight_report_name',
        ),
    ]