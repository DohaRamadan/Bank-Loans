from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from bank_personnel.models import *
from bank_personnel.serializers import *
from bank_personnel.permissions import *
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from .views import getRole, getLoanApplication, getLoanFundApplication
from rest_framework import status



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
        self.loan_provider = User.objects.create_user(
            username='testuser10',
            password='testpassword',
            role='Loan Provider'
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
        self.loan_fund_application = LoanFundApplication.objects.create(
            amount = 20000, 
            customer = self.loan_provider,
            status = 'Approved'
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


class LoanViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='Loan Customer'
        )

    def test_make_payment(self):
        self.user.available_amount = 10000
        self.client.force_authenticate(user=self.user)
        payment_data = {
            'amount': 1000
        }
        response = self.client.post(reverse('loans-make-payment'), payment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        payment = LoanPayment.objects.get(id=response.data['id'])
        self.assertEqual(payment.loan_customer, self.user)
        self.assertEqual(payment.amount, 1000)

        self.user.refresh_from_db()
        self.assertEqual(self.user.available_amount, 9000)

        serialized_payment = LoanPaymentSerializer(payment)
        self.assertEqual(response.data, serialized_payment.data)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.loan = Loan.objects.create(
            min_amount=1000,
            max_amount=10000,
            interest_rate=5,
            duration=12
        )
    
    def test_getRole_authenticated_user(self):
        request = self.factory.get('/role/')
        force_authenticate(request, user=self.user)
        
        response = getRole(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'role': self.user.role})
    
    def test_getRole_unauthenticated_user(self):
        request = self.factory.get('/role/')
        
        response = getRole(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'error': 'user not authenticated'})
    
    def test_getLoanApplication_existing_application(self):
        loan_application = LoanApplication.objects.create(id=1, customer= self.user, loan = self.loan, amount = 1000)
        
        request = self.factory.get('/loan_application/1/')
        
        response = getLoanApplication(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, LoanApplicationSerializer(loan_application).data)
    
    def test_getLoanApplication_nonexisting_application(self):
        request = self.factory.get('/loan_application/1/')
        
        response = getLoanApplication(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'error': 'Loan Application does not exist'})
    
    def test_getLoanFundApplication_existing_application(self):
        loan_fund_application = LoanFundApplication.objects.create(id=1, customer=self.user, amount = 10000)
        
        request = self.factory.get('/loan_fund_application/1/')
        
        response = getLoanFundApplication(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, LoanFundApplicationSerializer(loan_fund_application).data)
    
    def test_getLoanFundApplication_nonexisting_application(self):
        request = self.factory.get('/loan_fund_application/1/')
        
        response = getLoanFundApplication(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'error': 'Loan Fund Application does not exist'})





class GetAvailableAmountTestCase(APITestCase):

    def test_get_available_amount_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        response = self.client.get('/get-available-amount', follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {'available_amount': user.available_amount})

    def test_get_available_amount_unauthenticated(self):
        response = self.client.get('/get-available-amount', follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {'error': 'user not authenticated'})