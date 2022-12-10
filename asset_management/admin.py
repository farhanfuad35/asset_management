from django.contrib import admin
from .models import Asset, AssetTypes, Log

# Register your models here.
admin.site.register(Asset)
admin.site.register(AssetTypes)
admin.site.register(Log)
