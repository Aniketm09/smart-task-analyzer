from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    due_date = serializers.CharField(required=False, allow_null=True)
    estimated_hours = serializers.FloatField(required=False)
    importance = serializers.IntegerField(required=False)
    dependencies = serializers.ListField(required=False)
