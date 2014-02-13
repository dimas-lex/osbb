from django import forms
from django.contrib.auth.models import User

from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput
from bootstrap3_datetime.widgets import DateTimePicker

from osb.billing.models import Accounts, Services

import logging
logger = logging.getLogger('osb')

class AccountShortModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountShortModelForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)

            if field:
                # fieldType = type(field.widget)
                attrs = {
                    'placeholder': field.help_text,
                    'ng-model': "account_model." + field_name.lower()
                }
                field.widget.attrs.update(attrs)

    class Meta:
        model = Accounts
        fields = ('uid','name', 'porch', 'floor', 'phone', 'relatives',)
        exclude = ('deleted', 'notes',)

class ServiceModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceModelForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)

            if field:
                fieldWidgeType = type(field.widget)
                attrs = {
                    'placeholder': field.help_text,
                    'ng-model': "service_model." + field_name.lower()
                }
                logger.debug(attrs)
                if fieldWidgeType == forms.widgets.DateInput:
                    field.widget=BootstrapDateInput(format = '%d.%m.%Y', attrs = attrs)
                else:
                    field.widget=forms.TextInput(attrs)

    class Meta:
        model = Services
        fields = ('id', 'name','service_count', 'price', 'start_date', 'end_date',)
        exclude = ('is_active', 'account',)


