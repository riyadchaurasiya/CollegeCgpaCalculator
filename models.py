from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    grade = models.CharField(max_length=2, choices=[('O', 'O'), ('A+', 'A+'), ('A', 'A'), ('B+', 'B+'), ('B', 'B'), ('C', 'C'), ('F', 'F')])
    credit = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - Grade: {self.grade}, Credit: {self.credit}"