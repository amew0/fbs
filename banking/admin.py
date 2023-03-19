from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CreditCardDetail)
admin.site.register(User)
# admin.site.register(Balance)
admin.site.register(Allowance)
admin.site.register(Bill)
admin.site.register(Debit)
admin.site.register(statement)