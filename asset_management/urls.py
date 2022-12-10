from django.urls import path, include
from .views import AssetListStock, AssetListNotInStock

api_urls = [
    path('asset_in_stock', AssetListStock.as_view()),
    path('asset_not_in_stock', AssetListNotInStock.as_view())
]

urlpatterns = [
    path('api/', include(api_urls))
]