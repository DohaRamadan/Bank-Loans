from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from bank_personnel.models import Loan, LoanApplication, LoanFundApplication
from bank_personnel.serializers import LoanSerializer, LoanApplicationSerializer, LoanFundApplicationSerializer
from bank_personnel.permissions import IsLoanCustomer, IsBankPersonnel, IsLoanProvider, IsLoanCustomerOrBankPersonnel, IsLoanProviderOrBankPersonnel

User = get_user_model()

class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_signup(self):
        url = reverse('signup')
        data = {"username": "testuser2", "password": "testpassword2", "email" : "testuser2@gmail.com" ,"role" : "Loan Customer"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login(self):
        url = reverse('login')
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('key', response.data)


class LoanViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='Bank Personnel'
        )
        self.loan = Loan.objects.create(
            min_amount=1000,
            max_amount=10000,
            interest_rate=5,
            duration=12
        )
        self.url = reverse('loans-view')

    def test_list_all_loans(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_add_loan(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'min_amount': 2000,
            'max_amount': 15000,
            'interest_rate': 6,
            'duration': 24
        }
        response = self.client.post(reverse('loans-submit'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 2)

    def test_add_loan_permission(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Loan Customer'
        )
        self.client.force_authenticate(user=user)
        data = {
            'min_amount': 2000,
            'max_amount': 15000,
            'interest_rate': 6,
            'duration': 24
        }
        response = self.client.post(reverse('loans-submit'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_all_loans_permission(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Loan Provider'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoanApplicationViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='Loan Customer'
        )
        self.loan = Loan.objects.create(
            min_amount=1000,
            max_amount=10000,
            interest_rate=5,
            duration=12
        )
        self.loan_application = LoanApplication.objects.create(
            customer=self.user,
            loan=self.loan,
            amount=5000
        )
        self.url = reverse('loan-applications-view')

    def test_submit_loan_application(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'loan': self.loan.id,
            'amount': 7500
        }
        response = self.client.post(reverse('loan-applications-submit'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoanApplication.objects.count(), 2)

    def test_approve_or_reject_loan_application(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Bank Personnel'
        )
        self.client.force_authenticate(user=user)
        data = {"status": "Approved"}
        response = self.client.put(reverse('loan-applications-update', args=[self.loan_application.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.loan_application.refresh_from_db()
        self.assertEqual(self.loan_application.status, 'Approved')

    def test_approve_or_reject_loan_application_permission(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Loan Customer'
        )
        self.client.force_authenticate(user=user)
        data = {"status": "Rejected"}
        response = self.client.put(reverse('loan-applications-update', args=[self.loan_application.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_all_loan_applications(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Bank Personnel'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        loan_applications = LoanApplication.objects.all()
        serializer = LoanApplicationSerializer(loan_applications, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_all_loan_applications_permission(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Loan Provider'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoanFundApplicationViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='Loan Provider'
        )
        self.loan_fund_application = LoanFundApplication.objects.create(
            customer=self.user,
            amount=100000
        )
        self.url = reverse('loan-fund-applications-view')

    def test_submit_loan_fund_application(self):
        self.client.force_authenticate(user=self.user)
        data = {'amount': 50000}
        response = self.client.post(reverse('loan-fund-applications-submit'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoanFundApplication.objects.count(), 2)

    def test_approve_or_reject_loan_fund_application(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Bank Personnel'
        )
        self.client.force_authenticate(user=user)
        data = {"status": "Approved"}
        response = self.client.put(reverse('loan-fund-applications-update', args=[self.loan_fund_application.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.loan_fund_application.refresh_from_db()
        self.assertEqual(self.loan_fund_application.status, 'Approved')

    def test_approve_or_reject_loan_fund_application_permission(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Loan Customer'
        )
        self.client.force_authenticate(user=user)
        data = {"status": "Rejected"}
        response = self.client.put(reverse('loan-fund-applications-update', args=[self.loan_fund_application.id]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_all_loan_fund_applications(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Bank Personnel'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        loan_fund_applications = LoanFundApplication.objects.all()
        serializer = LoanFundApplicationSerializer(loan_fund_applications, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_all_loan_fund_applications_permission(self):
        user = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            role='Loan Customer'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)