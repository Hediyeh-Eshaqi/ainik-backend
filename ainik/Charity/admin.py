from django.contrib import admin
from.models import CharityWork, Charity, UserCharity

# Register your models here.
admin.site.register(Charity)
admin.site.register(CharityWork)
admin.site.register(UserCharity)