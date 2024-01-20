from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Pose(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='poses')
    created_at = models.DateTimeField(auto_now_add=True)
    accuracy_score = models.IntegerField(
        default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    class Meta:
        ordering = ["-accuracy_score", "created_at"]
