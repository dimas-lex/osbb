# -*- coding: utf-8 -*-
from django.db import models
import logging
import re

logger = logging.getLogger('osb')


class Accounts(models.Model):
    uid = models.CharField(max_length=20, unique=True, verbose_name=u"Квартира №", help_text="Уникальный Идентификатор Владельца")
    name = models.CharField(max_length=50, verbose_name=u"ФИО", help_text="Фамилия и Имя Владельца ")
    address = models.CharField(max_length=60, blank=True, null=True, verbose_name=u"Адресс", help_text="Адресс", default="пр. Мира 89 ")
    porch = models.IntegerField(blank=True, null=True, default=1, verbose_name=u"Подъезд", help_text="")
    floor = models.IntegerField(blank=True, null=True, default=1, verbose_name=u"Этаж", help_text="")
    # company = models.CharField(max_length=2,
    #                                   choices=( ('0', 'OSB'), ('1', 'Sokol') ),
    #                                   default='0', verbose_name=u"", help_text="")
    # city = models.CharField(max_length=60, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"Домашний Телефон", help_text="Домашний Телефон")
    relatives = models.TextField(blank=True, null=True, verbose_name=u"Другие Жильци Квартиры", help_text="")
    notes = models.TextField(blank=True, null=True, verbose_name=u"Поле для Заметок")
    deleted = models.BooleanField(default=False)

    def __lt__(self, other):
        regex_pat = re.compile(r'(\d+)')

        try:
            flatA = re.findall(regex_pat, self.uid)
            flatB = re.findall(regex_pat, other.uid)
            flatA.append(0)
            flatB.append(0)

            nubA = flatA.pop(0)
            nubB = flatB.pop(0)

            if (nubA == nubB):
                nubA = flatA.pop(0) or 0
                nubB = flatB.pop(0) or 0

            return int(nubA) < int(nubB)
        except AttributeError:
            return 0

    def __gt__(self, other):
        return not self.__lt__(other)

class Services(models.Model):
    """model for account's Services"""
    name = models.CharField(max_length=50, default="Квартплата", verbose_name="Название сервиса", help_text="Название сервиса")
    service_count = models.DecimalField (max_digits=5, decimal_places=2, default=0, verbose_name=u"Площадь", help_text="Название сервиса")

    def __init__(self, arg):
        super(Services, self).__init__()
        self.arg = arg
