# Generated by Django 2.1.1 on 2018-09-19 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ov', '0003_auto_20180913_0223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_outing', models.CharField(max_length=50)),
                ('hostelblock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ov.HostelBlock')),
            ],
        ),
    ]
