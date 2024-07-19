from django.db import models


class ExampleDatabaseModel(models.Model):
    foo = models.CharField(max_length=100)
    bar = models.IntegerField()
