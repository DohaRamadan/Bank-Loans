"""
URL configuration for bank_loans project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bank_personnel.views import *

from django.conf import settings  
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from bank_personnel import views

from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from bank_personnel.viewsets import *



urlpatterns = [
    path('loans/submit/', LoanViewSet.as_view({'post': 'add_loan'}), name='loans-submit'),
    path('loans/view/', LoanViewSet.as_view({'get': 'list_all_loans'}), name='loans-view'),
    path('loan-applications/submit/', LoanApplicationViewSet.as_view({'post': 'submit_loan_application'}), name='loan-applications-submit'),
    path('loan-applications/update/<int:pk>/', LoanApplicationViewSet.as_view({'put': 'approve_or_reject_loan_application'}), name='loan-applications-update'),
    path('loan-applications/view/', LoanApplicationViewSet.as_view({'get': 'list_loan_applications'}), name='loan-applications-view'),
    path('loan-fund-applications/submit/', LoanFundApplicationViewSet.as_view({'post': 'submit_loan_fund_application'}), name='loan-fund-applications-submit'),
    path('loan-fund-applications/update/<int:pk>/', LoanFundApplicationViewSet.as_view({'put': 'approve_or_reject_loan_fund_application'}), name='loan-fund-applications-update'),
    path('loan-fund-applications/view/', LoanFundApplicationViewSet.as_view({'get': 'list_loan_fund_applications'}), name='loan-fund-applications-view'),
    path('signup/', views.signup, name='signup'),
    path("signin/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("user/", UserDetailsView.as_view()), 
    path('admin/', admin.site.urls),
]