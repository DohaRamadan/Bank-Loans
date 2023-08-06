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
    path('loans/make-payment/', LoanPaymentViewSet.as_view({'post': 'make_payment'}), name='loans-make-payment'),
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
    path('get-user-role/', views.getRole), 
    path('get-available-amount/', views.getAvailableAmount), 
    path('loan-applications/get/<int:pk>/', views.getLoanApplication),
    path('loan-fund-applications/get/<int:pk>/', views.getLoanFundApplication), 
]