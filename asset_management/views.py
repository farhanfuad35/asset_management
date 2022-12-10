from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from user_management.permissions import IsCompanyAdmin, IsEmployee, IsSoftwareAdmin
from .models import Asset, AssetTypes, Log
from .serializers import *
import json
from rest_framework.response import Response

# Currently in Stock Assets
class AssetListStock(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin | IsSoftwareAdmin]
    serializer_class = AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.filter(company=self.request.user.employee.company, in_stock=True)


# Currently Not in Stock Assets
class AssetListNotInStock(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin | IsSoftwareAdmin]
    serializer_class = AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.filter(company=self.request.user.employee.company, in_stock=False)


# All Asset details for each company (or reagarless for Software Admins)
class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    permission_classes = [IsCompanyAdmin | IsSoftwareAdmin]

    def get_queryset(self):
        # Implies that the user is Software Admin
        if hasattr(self.request.user, 'is_staff') or hasattr(self.request.user, 'is_superuser'):
            return Asset.objects.all()
        # Implies that the user is a company admin
        else:
            return Asset.objects.filter(company=self.request.user.employee.company)



# Asset History/Log
class LogViewCompany(generics.ListAPIView):
    serializer_class = LogSerializer
    permission_classes = [IsCompanyAdmin]

    def get_queryset(self):
        return Log.objects.filter(asset__company=self.request.user.employee.company)

class LogViewAsset(generics.ListAPIView):
    serializer_class = LogSerializer
    permission_classes = [IsCompanyAdmin]

    def get_queryset(self):
        pk = self.request.parser_context['kwargs']['id']
        return Log.objects.filter(asset__company=self.request.user.employee.company, asset=pk)



# Assign Asset to an Employee
class AssignAssetView(APIView):
    '''
    Assigns an asset to an employee. Expects a POST request with fields
    'employee_id' and 'asset_id' which are the object id ('ID' field in list response)
    of employee and the asset respectively.
    '''

    permission_classes = [IsCompanyAdmin]

    def isCompanyEmployee(self, company, employee_id):
        try:
            employee = Employee.objects.get(pk=employee_id)
            return employee.company == company and employee.in_service
        except Employee.DoesNotExist:
            return False

    def isCompanyAsset(self, company, asset_id):
        try:
            asset = Asset.objects.get(pk=asset_id)
            return asset.company == company and asset.in_stock
        except Asset.DoesNotExist:
            return False

    def post(self, request):
        try:
            req_obj = request.data
            employee_id = req_obj['employee_id']
            asset_id = req_obj['asset_id']
            if(self.isCompanyAsset(self.request.user.employee.company, asset_id) and self.isCompanyEmployee(self.request.user.employee.company, employee_id)):
                asset = Asset.objects.get(pk=asset_id)
                employee = Employee.objects.get(pk=employee_id)
                asset.assign_to(employee)
                return Response({'message': 'Successfully assigned to the employee'}, status=200)
            else:
                return Response({'error': 'You do not have permission for this action'}, status=401)
        
        except Exception as e:
            print(e)
            return Response({'error': 'Server Error Occurred'}, status=400)


# Receive Asset from an Employee
class ReturnAssetView(APIView):
    '''
    Expects a POST request with Form-Field 'asset_id' which is the Object ID of the asset (pk).
    Not the company assigned asset_id.
    '''
    permission_classes = [IsCompanyAdmin]

    def isCompanyAsset(self, company, asset_id):
        try:
            asset = Asset.objects.get(pk=asset_id)
            return asset.company == company
        except Asset.DoesNotExist:
            return False

    def post(self, request):
        try:
            req_obj = request.data
            asset_id = req_obj['asset_id']
            if(self.isCompanyAsset(self.request.user.employee.company, asset_id)):
                asset = Asset.objects.get(pk=asset_id)
                asset.returned_to_company()
                return Response({'message': 'Asset recieved successfullt'}, status=200)
            else:
                return Response({'error': 'You do not have permission for this action'}, status=401)
        
        except Exception as e:
            print(e)
            return Response({'error': 'Server Error Occurred'}, status=400)



