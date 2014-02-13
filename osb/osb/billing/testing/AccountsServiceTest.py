# -*- coding: utf-8 -*-

from django.test import TestCase
from osb.billing.models import Accounts, Services
# from osb.billing.Services.AccountsService import AccountsService
from osb.billing.Services.AccountsService import AccountsService
from osb.billing.Services.ServiceService import *

class AccountsServiceTest(TestCase):
    def setUp(self):
        self.accountServ = AccountsService()
        self.accountServ.create(uid="1", name="lion", address="pr")
        self.accountServ.create(uid="2", name="cat", address="pr2")
        self.accountServ.create(uid="3", name="cat", address="pr2", porch=3)

    def test_01_get_all(self):
        """ Test 'get_all' method """
        print self.test_01_get_all.__doc__

        self.assertEqual(len(self.accountServ.get_all()), 3)

    def test_02_get_by_porch(self):
        """ Test 'get_by_porch' method """
        print self.test_02_get_by_porch.__doc__

        self.assertEqual(len(self.accountServ.get_by_porch(porch=3)), 1)

    def test_03_create(self):
        """ Test 'create' method """
        print self.test_03_create.__doc__

        self.assertTrue(
            isinstance(
                self.accountServ.create(uid="4", name="dog", address="pr"),
                Accounts
            )
        )

    def test_04_update(self):
        """ Test 'update' method """
        print self.test_04_update.__doc__

        self.assertTrue( self.accountServ.update(name="dog", uid="3", address="prr") )

    def test_05_delete(self):
        """ Test 'delete' method """
        print self.test_05_delete.__doc__

        self.assertTrue( self.accountServ.delete(uid="3")                            )

    # def test_06_print(self):
    #     """ Just #print out results """
    #     print self.test_06_print.__doc__

    #     accounts = self.accountServ.get_all()
    #     for acc in accounts:
    #         print ( " ".join(("uid", acc.uid, "name", acc.name, "address", acc.address, "porch", str(acc.porch), "deleted", str(acc.deleted) ))  )

    #     self.assertTrue(True)