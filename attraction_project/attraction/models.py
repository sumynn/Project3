from django.db import models

# Create your models here.


class CountryInfo(models.Model):
    country_no = models.IntegerField(primary_key=True)
    country_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country_info'


class ScoreInfo(models.Model):
    score_no = models.IntegerField(primary_key=True)
    country_name = models.CharField(max_length=45, blank=True, null=True)
    score = models.CharField(max_length=6, blank=True, null=True)
    vader_neg = models.CharField(max_length=6, blank=True, null=True)
    vader_neu = models.CharField(max_length=6, blank=True, null=True)
    vader_pos = models.CharField(max_length=6, blank=True, null=True)
    vader_com = models.CharField(max_length=6, blank=True, null=True)
    coutnry_no = models.ForeignKey(
        CountryInfo, models.DO_NOTHING, db_column='coutnry_no', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'score_info'


class Status(models.Model):
    country = models.CharField(primary_key=True, max_length=45)
    cases = models.IntegerField(blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    today_cases = models.IntegerField(
        db_column='today_cases', blank=True, null=True)
    cases_per_million = models.IntegerField(blank=True, null=True)

    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'


class Vaccine(models.Model):
    country = models.CharField(primary_key=True, max_length=32)
    vaccinated = models.IntegerField(blank=True, null=True)
    fully_vaccinated = models.IntegerField(blank=True, null=True)
    vaccination_rate = models.FloatField(blank=True, null=True)
    fully_vaccination_rate = models.FloatField(blank=True, null=True)

    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vaccine'
