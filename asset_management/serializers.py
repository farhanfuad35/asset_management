from rest_framework import serializers
from .models import *

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


class LogSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()
    owner = serializers.StringRelatedField()
    distributed_at = serializers.SerializerMethodField()
    recieved_at = serializers.SerializerMethodField()

    def get_distributed_at(self, obj):
        return obj.distributed_at.strftime("%d-%m-%Y %I:%M:%S %p")

    def get_recieved_at(self, obj):
        try:
            return obj.recieved_at.strftime("%d-%m-%Y %I:%M:%S %p")
        except Exception as e:
            print(e)
            return None

    class Meta:
        model = Log
        fields = ['asset', 'owner', 'distributed_at', 'recieved_at']