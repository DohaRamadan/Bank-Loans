from django.contrib import admin
from . import models

admin.site.register(models.Loan)
admin.site.register(models.LoanApplication)
admin.site.register(models.LoanFundApplication)
admin.site.register(models.CustomUser)
admin.site.register(models.LoanPayment)


