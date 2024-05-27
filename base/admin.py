from django.contrib import admin

from base import models

# Register your models here.

admin.site.site_header = ''
admin.site.site_title = 'Django Project'

admin.site.register(
    [
        models.PasswordValidationCode
    ]
)