# -*- coding: utf-8 -*-
from django.db import transaction, Error
from osb.billing.models import Accounts


import json
import logging
logger = logging.getLogger('osb')

class AccountsService(object):
    """
        AccountsService
        Class which operate with Accounts models
    """

    def get_all(self):
        return Accounts.objects.all()

    def get_by_porch(self, porch=None):
        """ The method return all active accounts for given porch """
        if (porch):
            try:
                return Accounts.objects.filter(porch=porch, deleted=False)
            except Error as ex:
                logger.error("While getting Accounts for porch error: " + str(porch))
        return list()

    @transaction.atomic
    def get_by_id(self, id=None):
        if (id):
            try:
                return Accounts.objects.get(id=id)
            except Accounts.DoesNotExist as ex:
                logger.error("Account does not exist with id " + str(id))

        return False

    @transaction.atomic
    def get_by_uid(self, uid=None):
        if (id):
            try:
                return Accounts.objects.get(uid=uid)
            except Error as ex:
                logger.error("Account does not exist with uid " + str(uid))

        return False

    @transaction.atomic
    def create(self, **kwargs):
        if ('uid' in kwargs and 'name' in kwargs):

            try:
                account = Accounts.objects.create(**kwargs)
            except Error as ex:
                return False

            return account

        return False

    @transaction.atomic
    def update(self, **kwargs):
        account = None

        if ('id' in kwargs):
            account = self.get_by_id(kwargs['id'])
            del kwargs.id

        elif ('uid' in kwargs):
            account = self.get_by_uid(kwargs['uid'])

        if (account):
            try:
                for key, value in kwargs.iteritems():
                    if (key != 'id'):
                        setattr(account, key, value)
                    account.save()
                return account

            except Error as ex:
                return False

        return False

    @transaction.atomic
    def delete(self, **kwargs):
        account = None

        if ('id' in kwargs):
            account = self.get_by_id(kwargs['id'])
            del kwargs.id

        elif ('uid' in kwargs):
            account = self.get_by_uid(kwargs['uid'])

        if (account):
            try:
                account.deleted = True
                account.save()
                return account

            except Error as ex:
                return False

        return False
