# Generated by Django 2.2.3 on 2019-08-01 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20190801_0616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oversight',
            name='overisght_checklist_year',
        ),
        migrations.RemoveField(
            model_name='template',
            name='oversight_name',
        ),
        migrations.AddField(
            model_name='oversight',
            name='areas',
            field=models.ManyToManyField(to='core.Area', verbose_name='Areas'),
        ),
        migrations.AddField(
            model_name='oversight',
            name='business_unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.BU', verbose_name='Business Unit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oversight',
            name='close_year',
            field=models.DateTimeField(null=True, verbose_name='Year'),
        ),
        migrations.AddField(
            model_name='oversight',
            name='country_office',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.CO', verbose_name='Country Office'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oversight',
            name='oversight_status',
            field=models.CharField(choices=[('new', 'New'), ('ongoing', 'Ongoing'), ('follow_up', 'Follow Up'), ('closed', 'Closed')], default=1, max_length=50, verbose_name='Status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oversight',
            name='regional_office',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.RO', verbose_name='Regional Office'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oversight',
            name='sections',
            field=models.ManyToManyField(to='core.Section', verbose_name='Sections'),
        ),
    ]