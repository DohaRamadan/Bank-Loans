from rest_framework import serializers
from .models import *


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
    def validate(self, data):
        if data['min_amount'] > data['max_amount']:
            raise serializers.ValidationError("Minimum amount cannot be greater than maximum amount")
        if data['interest_rate'] <= 0:
            raise serializers.ValidationError("Interest rate cannot be zero or negative")
        if data['duration'] <= 0:
            raise serializers.ValidationError("Duration cannot be zero or negative")
        return data
    
    def create(self, validated_data):
        loan = Loan.objects.create(
            min_amount=validated_data['min_amount'],
            max_amount=validated_data['max_amount'],
            interest_rate=validated_data['interest_rate'],
            duration=validated_data['duration']
        )
        return loan


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields =  '__all__'

    def validate(self, data):
        loan = Loan.objects.filter(id=data['loan'].id).first()
        if not loan:
            raise serializers.ValidationError("Loan does not exist")
        if data['amount'] > loan.max_amount:
            raise serializers.ValidationError("Loan amount cannot be greater than the maximum amount")
        if data['amount'] < loan.min_amount:
            raise serializers.ValidationError("Loan amount cannot be less than the minimum amount")
        
        return data
    
    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        loan_application = LoanApplication.objects.create(**validated_data)
        return loan_application


class LoanFundApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFundApplication
        fields = '__all__'

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount cannot be zero or negative")
        return data
    
    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        loan_fund_application = LoanFundApplication.objects.create(**validated_data)
        return loan_fund_application
    


class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser  
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user