# -*- coding: utf-8 -*-
from django.db import transaction, Error
from osb.billing.models import Accounts, Services
from osb.billing.Services.AccountsService import  AccountsService

import datetime
import json
import logging
logger = logging.getLogger('osb')

class  ServiceService(object):
    """
        ServiceService
        Class which operate with Services for Accounts models
    """
    @transaction.atomic
    def get_by_id(self, id=None):
        if (id):
            try:
                return Services.objects.get(id=id)
            except Services.DoesNotExist as ex:
                logger.error("Services does not exist with id " + str(id))

        return False

    def prepare_account(self, account):
        if (type(account) == int):
            account = AccountsService().get_by_id(account)
        if isinstance(account, Accounts):
            return account
        return False

    def prepare_service(self, service):
        if (type(service) == int):
            service = self.get_by_id(account)
        if isinstance(service, Services):
            return service
        return False


    def get_all(self):
        return Services.objects.all()

    def get_all_by_account(self, account):
        return Services.objects.filter(account=account)


    def create(self, data, account):
        """create a new active service for active (not deleted) account
            and return created service """
        account = self.prepare_account(account)
        if (not account or account.deleted): return False

        prev_service = account.get_active_service()
        if (prev_service):
            return self.update(data, account)

        return account.services.create(**data)

    def update(self, data, account):
        """ update account to new service and
            return created service if successful created """
        account = self.prepare_account(account)
        if not account: return False

        prev_service = account.get_active_service()
        if (not prev_service):
            return self.create(data, account)

        prev_service.is_active = False;
        bill_end_date = self.get_bill_end_date()
        prev_service.end_date = bill_end_date - datetime.timedelta (days = 1)
        prev_service.save()

        data['account'] = account
        data['start_date'] = bill_end_date
        if hasattr(data,'end_date'): del date['end_date']

        return Services.objects.create(**data)

    def get_bill_end_date(self):
        today = datetime.date.today()
        bill_end_date = today.replace(month=today.month + 1, day=1)
        return bill_end_date

    def cancel(self, service):
        """ cancel (turn off) active service and
            return service if successful canceled"""
        service = self.prepare_service(service)
        if (not service): return False

        service.end_date = self.get_bill_end_date()
        service.is_active = False
        service.save()

        return service