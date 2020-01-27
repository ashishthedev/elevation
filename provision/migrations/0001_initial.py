# Generated by Django 2.2.9 on 2020-01-26 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provisioner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('state', models.CharField(blank=True, choices=[('SUCCESS', 'SUCCESS'), ('FAILURE', 'FAILURE'), ('WIP', 'WIP')], max_length=10)),
                ('started_at', models.DateTimeField()),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('time_taken', models.DurationField(blank=True, null=True)),
            ],
        ),
    ]