from django.test import TestCase
from .models import *
import json
from user_management.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class Factory():
    def create_instances(self):
        user = User.objects.create_user(username='rahat', password='password')
        user2 = User.objects.create_user(username='brotee', password='password')
        company = Company.objects.create(name='Therap BD', address='Banani, Dhaka', contact_no='01786476455')
        employee_admin = Employee.objects.create(user=user, employee_id=17, company=company, is_company_admin=True, in_service=True)
        employee = Employee.objects.create(user=user2, employee_id=12, company=company, is_company_admin=False, in_service=True)
        assetType = AssetTypes.objects.create(name='Laptop')
        asset = Asset.objects.create(company=company, asset_id=67, asset_type=assetType, in_stock=True)
        asset = Asset.objects.create(company=company, asset_id=84, asset_type=assetType, in_stock=False)
        asset = Asset.objects.create(company=company, asset_id=23, asset_type=assetType, in_stock=False)

        return (user, user2, company, employee, employee_admin, asset)

class AssetTest(TestCase):
    def setUp(self):
        factory = Factory()
        (self.user1, self.user2, self.compnay, self.employee, self.employee_admin, self.asset) = factory.create_instances()
        self.token_user1 = Token.objects.create(user=self.user1)
        self.token_user2 = Token.objects.create(user=self.user2)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)

    def test_asset_in_stock(self):
        # token_url = "/api-token-auth/"
        # token = self.client.post(path=token_url, data={"username": "rahat", "password": "password"})
        # token = token.json()
        # token = token['token']
        target_url = "/asset/api/asset_in_stock"
        response = self.client.get(path=target_url)
        self.assertEqual(response.status_code, 200)
        
        response = response.json()
        self.assertEqual(len(response), 1)

    def test_asset_not_in_stock(self):
        target_url = "/asset/api/asset_not_in_stock"
        response = self.client.get(path=target_url)
        self.assertEqual(response.status_code, 200)
        
        response = response.json()
        self.assertEqual(len(response), 2)

    def test_asset_in_stock_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user2.key)
        target_url = "/asset/api/asset_in_stock"
        response = self.client.get(path=target_url)
        self.assertEqual(response.status_code, 403)
        