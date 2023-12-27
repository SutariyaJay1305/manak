from django.contrib import admin
from .models import UserPayment

# Register your models here.


class UserPaymentAdmin(admin.ModelAdmin):
    pass



admin.site.register(UserPayment, UserPaymentAdmin)
