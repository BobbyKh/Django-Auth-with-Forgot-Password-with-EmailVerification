from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PasswordValidationCode(models.Model):
    # Add your custom fields here
    validation_code = models.CharField(max_length=6, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.validation_code
