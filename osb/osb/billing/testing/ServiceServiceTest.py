# -*- coding: utf-8 -*-
from django.test import TestCase
from osb.billing.models import Accounts, Services
from osb.billing.Services.AccountsService import AccountsService
from osb.billing.Services.ServiceService import ServiceService

class ServiceServiceTest(TestCase):

    def setUp(self):
        self.account_serv = AccountsService()
        self.test_account = self.account_serv.create(uid="1", name="lion", address="pr")
        self.serv_services = ServiceService()
        self.service_data = {
            'name': 'KV',
            'service_count': 20,
            'price': 1.1
        }

    def test_01_create(self):
        """ test creation of a new active service for active (not deleted) account"""
        print (self.test_01_create.__doc__)

        service = self.serv_services.create(self.service_data, self.test_account)
        self.assertEqual(service, self.test_account.get_active_service())

    def test_02_create(self):
        """ test creation of a new service for unknown account """
        print (self.test_02_create.__doc__)

        service = self.serv_services.create(self.service_data, -1000112)
        self.assertFalse(service)

    def test_03_update(self):
        """ test updating of a account to new service """
        print (self.test_03_update.__doc__)

        old_serv = self.serv_services.create(self.service_data, self.test_account)

        self.service_data['service_count'] = 22
        service = self.serv_services.update(self.service_data, self.test_account)

        self.assertEqual(service, self.test_account.get_active_service())

    def test_04_cancel(self):
        """ test cancellation (turning off) of active service """
        print (self.test_04_cancel.__doc__)

        services = self.serv_services.create(self.service_data, self.test_account)

        services = self.serv_services.cancel(services)

        self.assertEqual(self.test_account.get_active_service(), None)

    # def test_06_print(self):
    #     """ Just print out results """
    #     print self.test_06_print.__doc__
    #     services = self.test_account.services.all()
    #     print self.test_account.get_active_service()
    #     for srv in services:
    #         print(srv)
    #     self.assertEqual(1, 1)
