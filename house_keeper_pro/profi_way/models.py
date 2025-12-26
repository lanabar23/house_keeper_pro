from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('in_progress', 'В работе'),
        ('completed', 'Завершен'),
        ('deferred', 'Отложен'),
    ])
    responsible = models.CharField(max_length=255)