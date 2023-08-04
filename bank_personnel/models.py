from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings  
from django.contrib.auth.models import AbstractUser
from django.conf import settings  


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)

class CustomUser(AbstractUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('Loan Provider', 'Loan Provider'),
        ('Loan Customer', 'Loan Customer'),
        ('Bank Personnel', 'Bank Personnel')
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )



class Loan(models.Model):
    min_amount = models.DecimalField(null=False, max_digits=18, decimal_places=3)
    max_amount = models.DecimalField(null=False, max_digits=18, decimal_places=3)
    interest_rate = models.DecimalField(null=False, max_digits=18, decimal_places=3)
    duration = models.IntegerField(null=False) #in months

class LoanApplication(models.Model):
    bank_personnel = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loan_applications_bank_personnel", on_delete=models.CASCADE, default=None, null=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loan_applications_customer", on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(null=False, max_digits=18, decimal_places=3)
    status = models.CharField(max_length=50, null=False, choices=STATUS_CHOICES, default="Pending")

class LoanFundApplication(models.Model):
    bank_personnel = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loan_fund_applications_bank_personnel", on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loan_fund_applications_customer", on_delete=models.CASCADE)
    amount = models.DecimalField(null=False, max_digits=18, decimal_places=3)
    status = models.CharField(max_length=50, null=False, choices=STATUS_CHOICES, default="Pending")
    



