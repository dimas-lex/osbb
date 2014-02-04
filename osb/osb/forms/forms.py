from django import forms
from django.contrib.auth.models import User
from osb.billing.models import Accounts
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput
import logging
logger = logging.getLogger('osb')

class AccountShortModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountShortModelForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            logger.debug(field_name + ":"+ str(field.required))
            logger.debug(field.widget)

            if field:
                fieldType = type(field.widget)
                attrs = {
                    'placeholder': field.help_text,
                    'ng-model': "account_model." + field_name.lower()
                }
                field.widget.attrs.update(attrs)

        #         if fieldType in (forms.TextInput, forms.DateInput):
        #              field.widget = forms.TextInput(attrs)

        #         if (fieldType == forms.NumberInput):
        #              field.widget = forms.NumberInput(attrs)

        #         if (fieldType == forms.Textarea):
        #              field.widget = forms.Textarea(attrs)

    class Meta:
        model = Accounts
        fields = ('uid','name', 'porch', 'floor', 'phone', 'relatives',)
        exclude = ('deleted', 'notes',)

class TestForm(forms.Form):
    subject = forms.CharField(max_length=100, help_text='Maximum 100 chars.')
    message = forms.CharField(required=False, help_text='<i>my_help_text</i>')
    sender = forms.EmailField()
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    cc_myself = forms.BooleanField(required=False, help_text='You will get a copy in your mailbox.')



    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data