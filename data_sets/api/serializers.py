from rest_framework import serializers

from ..models import DataSet


class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('name', 'users_id_sample', 'users_num', 'items_num', 'density', 'description')