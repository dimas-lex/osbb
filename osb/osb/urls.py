
from billing.views import *
from django.views.generic import TemplateView

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
    # url(r'^', include(router.urls)),
    # url(r'^accounts/remove$', delete_account),
    url(r'^accounts/(?P<page>\d{1})', get_accounts_for_page),
    # url(r'^accounts/add$', add_account),
    url(r'^accounts/', get_accounts_for_page),
    # url(r'^rest/accounts/add$', add_account),


)


urlpatterns += format_suffix_patterns(
    ( url(r'^rest/accounts/$',  AccountsList.as_view()), )
)