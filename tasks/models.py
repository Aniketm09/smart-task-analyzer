from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.FloatField(null=True, blank=True)
    importance = models.IntegerField(null=True, blank=True)
    dependencies = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title
