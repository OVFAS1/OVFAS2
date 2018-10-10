# Generated by Django 2.1.1 on 2018-09-19 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ov', '0006_filter_date_of_outing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='date_of_outing',
            field=models.CharField(blank=True, choices=[('0', '2018-09-23'), ('1', '2018-09-24')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='hostelblock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ov.HostelBlock'),
        ),
    ]
