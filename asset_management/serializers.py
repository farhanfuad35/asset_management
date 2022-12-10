from rest_framework import serializers
from .models import Asset

class AssetSerializer(serializers.ModelSerializer):
    '''
    Serializer inteded for the company admins. To see current status, check the log API
    '''
    # Returns the company name field in the JSON response
    company = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    asset_type = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = Asset 
        fields = ['id', 'company', 'asset_id', 'asset_type', 'manufacturer', 'purchased_at', 'purchased_from', 'current_owner']