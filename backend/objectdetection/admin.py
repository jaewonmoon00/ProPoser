from django.contrib import admin
from .models import Pose
# Register your models here.
class PoseAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'

admin.site.register(Pose, PoseAdmin)