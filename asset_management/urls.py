from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssetListStock, AssetListNotInStock, AssetViewSet, LogViewAsset, LogViewCompany, AssignAssetView, ReturnAssetView

router = DefaultRouter()
router.register('assets', AssetViewSet, basename='user')

api_urls = [
    path('asset_in_stock', AssetListStock.as_view()),
    path('asset_not_in_stock', AssetListNotInStock.as_view()), 
    path('log/company', LogViewCompany.as_view()),
    path('log/asset/<int:id>', LogViewAsset.as_view()),
    path('assign_asset', AssignAssetView.as_view()),
    path('return_asset', ReturnAssetView.as_view())
]

urlpatterns = [
    path('api/', include(api_urls))
]

urlpatterns+=router.urls