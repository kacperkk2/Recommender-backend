from rest_framework import serializers


class RecommendationElementSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    crag = serializers.CharField(max_length=50)
    sector = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=20)
    grade = serializers.CharField(max_length=5)