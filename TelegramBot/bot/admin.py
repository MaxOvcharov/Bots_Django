from django.contrib import admin

from models import Cities, CityPhotos, DialogStepRouting, UserInfo, CityPoll
# Register your models here.

admin.site.register(Cities)
admin.site.register(CityPhotos)
admin.site.register(DialogStepRouting)
admin.site.register(UserInfo)
admin.site.register(CityPoll)
