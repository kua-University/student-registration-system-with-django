from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student_name','email','course_name','amount')
    
    
admin.site.register(Payment,PaymentAdmin)
