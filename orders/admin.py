from django.contrib import admin

import orders.models as models

admin.site.register(models.Location)
admin.site.register(models.Restaurant)
