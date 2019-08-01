# Generated by Django 2.2.3 on 2019-08-01 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20190801_0526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oversight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oversight_name', models.CharField(max_length=100, verbose_name='Oversight Name')),
                ('overisght_checklist_year', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'Oversight',
            },
        ),
        migrations.RemoveField(
            model_name='template',
            name='oversight_report_name',
        ),
        migrations.AddField(
            model_name='template',
            name='oversight_name',
            field=models.CharField(default='name', max_length=100, verbose_name='Oversight Name'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='OversightReport',
        ),
        migrations.AddField(
            model_name='oversight',
            name='template',
            field=models.ManyToManyField(to='core.Template', verbose_name='Template'),
        ),
    ]