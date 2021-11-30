# Generated by Django 3.2.8 on 2021-11-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryInfo',
            fields=[
                ('country_no', models.IntegerField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'country_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ScoreInfo',
            fields=[
                ('score_no', models.IntegerField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(blank=True, max_length=45, null=True)),
                ('score', models.CharField(blank=True, max_length=45, null=True)),
                ('vader_neg', models.CharField(blank=True, max_length=45, null=True)),
                ('vader_neu', models.CharField(blank=True, max_length=45, null=True)),
                ('vader_pos', models.CharField(blank=True, max_length=45, null=True)),
                ('vader_com', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'score_info',
                'managed': False,
            },
        ),
    ]
