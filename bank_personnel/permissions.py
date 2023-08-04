from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsLoanProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Loan Provider'
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user

class IsLoanCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Loan Customer'
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user

class IsBankPersonnel(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Bank Personnel'
    
class IsLoanCustomerOrBankPersonnel(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'Loan Customer' or request.user.role == 'Bank Personnel')
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user

class IsLoanProviderOrBankPersonnel(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'Loan Provider' or request.user.role == 'Bank Personnel')
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user
    


    

    
