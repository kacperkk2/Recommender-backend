from django.db import models
from django.core.validators import int_list_validator

USERS_IDS_LIST_LENGTH = 10


class DataSet(models.Model):
    name = models.CharField(max_length=40, blank=True)
    short = models.CharField(max_length=40)
    users_id_sample = models.CharField(validators=[int_list_validator], max_length=USERS_IDS_LIST_LENGTH*10)
    users_num = models.CharField(max_length=10)
    items_num = models.CharField(max_length=10)
    density = models.CharField(max_length=10)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name