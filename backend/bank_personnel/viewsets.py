from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from .models import *
from .serializers import *
from .permissions import IsLoanCustomer, IsBankPersonnel, IsLoanProvider, IsLoanCustomerOrBankPersonnel, IsLoanProviderOrBankPersonnel
from decimal import Decimal


class LoanViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_permissions(self):
        if self.action == 'list_all_loans':
            permission_classes = [IsLoanCustomerOrBankPersonnel]
        elif self.action == 'add_loan':
            permission_classes = [IsBankPersonnel]
        elif self.action == 'make_payment': 
            permission_classes = [IsLoanCustomer] 
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['POST'], url_path='submit')
    def add_loan(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'], url_path='view')
    def list_all_loans(self, request):
        loans = Loan.objects.all()
        serializer = self.get_serializer(loans, many=True)
        return Response(serializer.data)
    

class LoanApplicationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer

    
    def get_permissions(self):
        if self.action == 'submit_loan_application':
            permission_classes = [IsLoanCustomer]
        elif self.action == 'approve_or_reject_loan_application':
            permission_classes = [IsBankPersonnel]
        else:
            permission_classes = [IsLoanCustomerOrBankPersonnel]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['POST'], url_path='submit')
    def submit_loan_application(self, request, pk=None):
        data = request.data.copy()  # Create a copy of the request data
        data['customer'] = request.user.pk  # Set the customer field,khj

        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'], url_path='update')
    def approve_or_reject_loan_application(self, request, pk=None):
        loan_application = self.get_object()
        loan_status = request.data.get('status')
        if loan_status in ['Approved', 'Rejected']:
            if request.user.role != 'Bank Personnel':
                raise PermissionDenied("You're not authorized to perform this action")
            loan_application.status = loan_status
            loan_application.bank_personnel = request.user
            loan_customer = loan_application.customer
            if loan_status == 'Approved':
                loan_customer.loan_amount += loan_application.amount
                loan_customer.save()
            try:
                loan_application.save()
            except ValidationError as e:
                loan_customer.loan_amount -= loan_application.amount
                loan_customer.save()
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)            

            serializer = self.get_serializer(loan_application)
            return Response(serializer.data)
        return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'],permission_classes = [IsLoanCustomerOrBankPersonnel], url_path='view')
    def list_loan_applications(self, request):
        if request.user.role == 'Bank Personnel' or request.user.is_admin:
            loan_applications = LoanApplication.objects.all()
        elif request.user.role == 'Loan Customer':
            loan_applications = LoanApplication.objects.filter(customer=request.user)
        else:
            raise PermissionDenied("You're not authorized to perform this action")
        serializer = self.get_serializer(loan_applications, many=True)
        return Response(serializer.data)
    
class LoanFundApplicationViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = LoanFundApplication.objects.all()
    serializer_class = LoanFundApplicationSerializer

    def get_permissions(self):
        if self.action == 'submit_loan_fund_application':
            permission_classes = [IsLoanProvider]
        elif self.action == 'approve_or_reject_loan_fund_application':
            permission_classes = [IsBankPersonnel]
        else:
            permission_classes = [IsLoanProviderOrBankPersonnel]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['POST'], url_path='submit')
    def submit_loan_fund_application(self, request, pk=None):
        data = request.data.copy()  # Create a copy of the request data
        data['customer'] = request.user.pk  # Set the customer field,khj
        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'], url_path='update')
    def approve_or_reject_loan_fund_application(self, request, pk=None):
        loan_fund_application = self.get_object()
        status = request.data.get('status')
        if status in ['Approved', 'Rejected']:
            loan_fund_application.status = status
            loan_fund_application.bank_personnel = request.user
            loan_fund_application.save()
            serializer = self.get_serializer(loan_fund_application)
            return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='view')
    def list_loan_fund_applications(self, request):
        if request.user.is_admin or request.user.role == 'Bank Personnel':
            loan_fund_applications = LoanFundApplication.objects.all()
        elif request.user.role == 'Loan Provider':
            loan_fund_applications = LoanFundApplication.objects.filter(customer=request.user)
        else:
            raise PermissionDenied("You're not authorized to perform this action")
        serializer = self.get_serializer(loan_fund_applications, many=True)
        return Response(serializer.data)
    



class LoanPaymentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = LoanPayment.objects.all()
    serializer_class = LoanPaymentSerializer

    def get_permissions(self):
        if self.action == 'make_payment':
            permission_classes = [IsLoanCustomer]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['POST'])
    def make_payment(self, request):
        amount = Decimal(request.data.get('amount', 0))
        if amount <= 0:
            return Response({'error': 'Invalid payment amount.'}, status=status.HTTP_400_BAD_REQUEST)
        if amount > request.user.loan_amount:
            return Response({'error': 'Payment amount exceeds the remaining loan amount.'},
								status=status.HTTP_400_BAD_REQUEST)
        loan_customer = request.user
        loan_customer.paid_amount += amount
        loan_customer.loan_amount -= amount
        loan_customer.save()
        loan_payment = LoanPayment.objects.create(
            loan_customer=loan_customer,
            amount=amount
        )
        serializer = self.get_serializer(loan_payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


        