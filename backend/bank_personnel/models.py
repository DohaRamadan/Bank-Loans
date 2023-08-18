from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings  
from django.contrib.auth.models import AbstractUser
from django.conf import settings  
from django.core.exceptions import ValidationError
from django.db.models import Sum



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
    paid_amount = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    loan_amount = models.DecimalField(max_digits=18, decimal_places=3, default=0)

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

    def __str__(self) -> str:
        return self.username



class Loan(models.Model):
    min_amount = models.DecimalField(null=False, max_digits=18, decimal_places=2)
    max_amount = models.DecimalField(null=False, max_digits=18, decimal_places=2)
    interest_rate = models.DecimalField(null=False, max_digits=18, decimal_places=2)
    duration = models.IntegerField(null=False) #in months


class LoanApplication(models.Model):
    bank_personnel = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loan_applications_bank_personnel", on_delete=models.CASCADE, default=None, null=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loan_applications_customer", on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(null=False, max_digits=18, decimal_places=3)
    status = models.CharField(max_length=50, null=False, choices=STATUS_CHOICES, default="Pending")

    def save(self, *args, **kwargs):
        total_loans = CustomUser.objects.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
        total_funds = LoanFundApplication.objects.filter(status='Approved').aggregate(Sum('amount'))['amount__sum'] or 0

        if total_loans > total_funds:
            raise ValidationError("Total loans exceed total funds.")

        super().save(*args, **kwargs)

class LoanFundApplication(models.Model):
    bank_personnel = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loan_fund_applications_bank_personnel", on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="loan_fund_applications_customer", on_delete=models.CASCADE)
    amount = models.DecimalField(null=False, max_digits=18, decimal_places=2)
    status = models.CharField(max_length=50, null=False, choices=STATUS_CHOICES, default="Pending")

class LoanPayment(models.Model):
    loan_customer = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="loan_payment_loan_customer" , on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    



