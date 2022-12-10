from django.shortcuts import render
from rest_framework import generics
from user_management.permissions import IsCompanyAdmin, IsEmployee, IsSoftwareAdmin
from .models import Asset, AssetTypes, Log
from .serializers import AssetSerializer

# Currently in Stock Assets
class AssetListStock(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin]
    serializer_class = AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.filter(company=self.request.user.employee.company, in_stock=True)


# Currently Not in Stock Assets
class AssetListNotInStock(generics.ListAPIView):
    permission_classes = [IsCompanyAdmin]
    serializer_class = AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.filter(company=self.request.user.employee.company, in_stock=False)


# Asset details by id



# Asset History/Log



# Assign Asset to an Employee



# Receive Asset from an Employee



# AssetType: CRUD



# Assets: CRUD



