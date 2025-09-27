from django.db import models

class Emdat(models.Model):
    historic = models.TextField(db_column='Historic', blank=True, null=True)
    classification_key = models.TextField(db_column='Classification Key', blank=True, null=True)
    disaster_group = models.TextField(db_column='Disaster Group', blank=True, null=True)
    disaster_type = models.TextField(db_column='Disaster Type', blank=True, null=True)
    iso = models.TextField(db_column='ISO', blank=True, null=True)
    country = models.TextField(db_column='Country', blank=True, null=True)
    start_year = models.BigIntegerField(db_column='Start Year', blank=True, null=True)
    total_deaths = models.FloatField(db_column='Total Deaths', blank=True, null=True)
    no_injured = models.FloatField(db_column='No. Injured', blank=True, null=True)
    no_affected = models.FloatField(db_column='No. Affected', blank=True, null=True)
    no_homeless = models.FloatField(db_column='No. Homeless', blank=True, null=True)
    total_affected = models.FloatField(db_column='Total Affected', blank=True, null=True)
    last_update = models.TextField(db_column='Last Update', blank=True, null=True)

    class Meta:
        db_table = 'emdat'

class KpiList(models.Model):
    domain = models.TextField(db_column='Domain', blank=True, null=True)
    sub_domain = models.TextField(db_column='Sub Domain', blank=True, null=True)
    sub_topic = models.TextField(db_column='Sub topic', blank=True, null=True)
    slr_indicator = models.TextField(db_column='SLR Indicator', blank=True, null=True)
    usability = models.TextField(db_column='Usability', blank=True, null=True)
    indicator = models.TextField(db_column='Indicator', blank=True, null=True)
    database = models.TextField(db_column='Database', blank=True, null=True)
    dataset_code = models.TextField(db_column='Dataset Code', blank=True, null=True)
    notes = models.TextField(db_column='Notes', blank=True, null=True)
    spatial_level = models.TextField(db_column='Spatial Level', blank=True, null=True)
    link = models.TextField(db_column='Link', blank=True, null=True)
    unnamed_11 = models.FloatField(db_column='Unnamed: 11', blank=True, null=True)
    unnamed_12 = models.FloatField(db_column='Unnamed: 12', blank=True, null=True)
    unnamed_13 = models.TextField(db_column='Unnamed: 13', blank=True, null=True)

    class Meta:
        db_table = 'kpi_list'

class Pca(models.Model):
    dataset_code = models.TextField(db_column='dataset_code', blank=True, null=True)
    geo = models.TextField(db_column='geo', blank=True, null=True)
    time = models.BigIntegerField(db_column='time', blank=True, null=True)
    values = models.FloatField(db_column='values', blank=True, null=True)

    class Meta:
        db_table = 'pca'
