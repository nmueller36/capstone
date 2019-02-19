from django.contrib import admin
from .models import PersonalInfo, AppData, AppAvailability, StudentPlacement, StudentSchedule, SiteInfo, SiteAvailability, SitePlacementRank

# Register your models here.
admin.site.register(PersonalInfo)
admin.site.register(AppData)
admin.site.register(AppAvailability)
admin.site.register(SitePlacementRank)
admin.site.register(StudentPlacement)
admin.site.register(StudentSchedule)
admin.site.register(SiteInfo)
admin.site.register(SiteAvailability)
