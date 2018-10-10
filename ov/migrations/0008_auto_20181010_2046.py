# Generated by Django 2.1.1 on 2018-10-10 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ov', '0007_auto_20180919_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='warden',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='filter',
            name='date_of_outing',
            field=models.CharField(blank=True, choices=[('0', '2018-10-14'), ('1', '2018-10-15')], max_length=50, null=True),
        ),
    ]
