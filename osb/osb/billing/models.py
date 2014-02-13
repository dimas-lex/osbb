# -*- coding: utf-8 -*-
from django.db import models
from datetime import date

import re
import logging
logger = logging.getLogger('osb')

class Accounts(models.Model):
    uid = models.CharField(max_length=20, unique=True, verbose_name="Квартира №", help_text="Уникальный Идентификатор Владельца")
    name = models.CharField(max_length=50, verbose_name="ФИО", help_text="Фамилия и Имя Владельца ")
    address = models.CharField(max_length=60, blank=True, null=True, verbose_name="Адресс", help_text="Адресс", default="пр. Мира 89 ")
    porch = models.IntegerField(blank=True, null=True, default=1, verbose_name="Подъезд", help_text="")
    floor = models.IntegerField(blank=True, null=True, default=1, verbose_name="Этаж", help_text="")
    # company = models.CharField(max_length=2,
    #                                   choices=( ('0', 'OSB'), ('1', 'Sokol') ),
    #                                   default='0', verbose_name=u"", help_text="")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Домашний Телефон", help_text="Домашний Телефон")
    relatives = models.TextField(blank=True, null=True, verbose_name="Другие Жильци Квартиры", help_text="")
    notes = models.TextField(blank=True, null=True, verbose_name="Поле для Заметок")
    deleted = models.BooleanField(default=False)

    def get_active_service(self):
        last_active = self.services.filter(is_active=True)
        return last_active[0] if (last_active) else None

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
    """Services for accounts"""
    name = models.CharField(max_length=50, default="Квартплата", verbose_name="Название сервиса", help_text="Название сервиса")
    service_count = models.DecimalField (max_digits=5, decimal_places=2, default=0, verbose_name=u"Площадь", help_text="Название сервиса")
    price = models.DecimalField(max_digits=7, decimal_places=5, default=0, verbose_name=u"Стоимость сервиса", help_text="Стоимость 1 сервиса")
    start_date = models.DateField(verbose_name=u"Врямя начала использования", help_text="С какого числа начислять плату за сервис", default=lambda: date.today().replace(day=1))
    end_date = models.DateField (verbose_name=u"Врямя конца использования", help_text="До какого числа начислять плату за сервис", default=date(2090, 01, 01), blank=True)
    is_active = models.BooleanField(default=True,)
    account =  models.ForeignKey(Accounts, related_name='services', related_query_name="services", on_delete=models.DO_NOTHING)


    def __unicode__(self):
        return ' : '.join(
            (self.name,
                str(self.service_count),
                str(self.price),
                str(self.start_date),
                str(self.end_date),
                str(self.is_active)
            )
        )
