# Generated by Django 2.2.3 on 2019-07-27 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190726_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='areas',
            field=models.ManyToManyField(null=True, to='core.Area'),
        ),
    ]
