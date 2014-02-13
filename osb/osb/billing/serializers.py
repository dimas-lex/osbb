from osb.billing.models import *
from rest_framework import serializers
import json
import logging
logger = logging.getLogger('osb')

class ServicesSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(source='start_date', format="%d.%m.%Y", input_formats=["%d.%m.%Y",])
    end_date = serializers.DateField(source='end_date', format="%d.%m.%Y", input_formats=["%d.%m.%Y",])
    class Meta:
        model = Services
        fields = ('id', 'name','service_count', 'price', 'start_date', 'end_date', 'account',)


class AccountsSerializer(serializers.ModelSerializer):
    services = ServicesSerializer(many=True, required=False)#
    class Meta:
        model = Accounts
        fields = ('id', 'uid','name', 'porch', 'floor', 'phone', 'relatives', 'notes', 'services',)



# class TrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Track
#         fields = ('order', 'title')

# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = TrackSerializer(many=True)

#     class Meta:
#         model = Album
#         fields = ('album_name', 'artist', 'tracks')