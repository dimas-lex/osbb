# -*- coding: utf-8 -*-
import unittest
from django.test import TestCase
from osb.billing.testing.AccountsServiceTest import  AccountsServiceTest
from osb.billing.testing.ServiceServiceTest import  ServiceServiceTest


class TestRunner(TestCase):
    def setUp(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(AccountsServiceTest)
        unittest.TextTestRunner(verbosity=1).run(suite)

        suite = unittest.TestLoader().loadTestsFromTestCase(ServiceServiceTest)
        unittest.TextTestRunner(verbosity=2).run(suite)


        # self.sServices.create(uid="1", name="lion", address="pr")
        # self.sServices.create(uid="2", name="cat", address="pr2")
        # self.sServices.create(uid="3", name="cat", address="pr2", porch=3)
