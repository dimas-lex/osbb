from osb.billing.models import *
from rest_framework import serializers
import logging,  json
logger = logging.getLogger('osb')

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ('id', 'uid','name', 'porch', 'floor', 'phone', 'relatives', 'notes',)
