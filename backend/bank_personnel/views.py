from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .permissions import *

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getRole(request):
    if request.user.is_authenticated:
        return Response({'role': request.user.role})
    else:
        return Response({'error': 'user not authenticated'})

# get Loan Application by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBankPersonnel])
def getLoanApplication(request, pk):
    try:
        loanApplication = LoanApplication.objects.get(id=pk)
        serializer = LoanApplicationSerializer(loanApplication, many=False)
        return Response(serializer.data)
    except:
        return Response({'error': 'Loan Application does not exist'})
    
# get Loan Fund Application by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsBankPersonnel])
def getLoanFundApplication(request, pk):
    try:
        loanFundApplication = LoanFundApplication.objects.get(id=pk)
        serializer = LoanFundApplicationSerializer(loanFundApplication, many=False)
        return Response(serializer.data)
    except:
        return Response({'error': 'Loan Fund Application does not exist'})
    
# get user loan_amount 
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getLoanAmount(request):
    if request.user.is_authenticated:
        return Response({'loan_amount': request.user.loan_amount})
    else:
        return Response({'error': 'user not authenticated'})

