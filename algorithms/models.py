from django.db import models


class Algorithm(models.Model):
    name = models.CharField(max_length=40, blank=True)
    short = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    link = models.TextField(blank=True)

    def __str__(self):
        return self.short
