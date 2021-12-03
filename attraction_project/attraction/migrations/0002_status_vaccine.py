# Generated by Django 3.2.8 on 2021-12-02 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attraction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('country', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('cases', models.IntegerField(blank=True, null=True)),
                ('today_cases', models.IntegerField(blank=True, db_column='today_cases', null=True)),
                ('cases_per_million', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('country', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('vaccinated', models.IntegerField(blank=True, null=True)),
                ('fully_vaccinated', models.IntegerField(blank=True, null=True)),
                ('vaccination_rate', models.FloatField(blank=True, null=True)),
                ('fully_vaccination_rate', models.FloatField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'vaccine',
                'managed': False,
            },
        ),
    ]
