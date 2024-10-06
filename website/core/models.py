from django.db import models

# Create your models here.

class fire(models.Model):
    date        = models.DateField(auto_now_add=True)
    file        = models.FileField(upload_to="firevideos/")
    percentage  = models.FloatField(default=0.0)
    time        = models.TimeField(auto_now_add=True)


    def __str__(self) -> str:
        return str(self.percentage)[:4]+"|"+str(self.date)