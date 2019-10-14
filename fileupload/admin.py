from django.contrib import admin

# Register your models here.
from fileupload.models import JsonFile, Tag

admin.site.register(JsonFile)
admin.site.register(Tag)