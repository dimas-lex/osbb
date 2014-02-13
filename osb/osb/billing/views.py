from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status, generics, permissions

from osb.billing.models import *
from osb.billing.serializers import *
from osb.forms.forms import *

import logging,  json
logger = logging.getLogger('osb')


class AccountsListView(APIView):
    """
        View class for managing and viewing Accounts
    """
    def get_object(self, id):
        try:
            return Accounts.objects.get(id=id)
        except Accounts.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        logger.debug('AccountsView get ------')

        page = request.GET.get('page', 1)
        accounts = Accounts.objects.filter(deleted = False) #, porch = page)
        serializer = AccountsSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        logger.debug('AccountsView post ------')

        if 'id' in request.POST:
            # update
            account = self.get_object(request.POST.get('id'))
            if account:
                serializer = AccountsSerializer(account, data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data , status=status.HTTP_201_CREATED)

        else:
            # 100 new account
            serializer = AccountsSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        # fail
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        logger.debug("AccountsView delete_account --")

        del_result = False
        account = None

        if request.method == 'DELETE':
            query_dict = request.GET

            try:
                if 'uid' in query_dict:
                    uid = query_dict.get('uid')
                    logger.debug("delete_account by uid: " + str(uid))
                    account = Accounts.objects.get(uid=uid)

                elif 'id' in query_dict:
                    id = query_dict['id']
                    logger.debug("delete_account by id: " + str(id))
                    account = Accounts.objects.get(id=id)
            except (Accounts.DoesNotExist) as ex:
                return Response(json.dumps({'success': del_result}))

            if account != None:
                try:
                    account.delete()
                    del_result = True
                except (Exception) as ex:
                    logger.error("ERROR: delete_account can't delete account" + json.dumps(request.GET))
                    logger.error(ex)

        return Response({'success': del_result} )

class AccountView(APIView):
    """docstring for AccountView"""
    def __init__(self, arg):
        super(AccountView, self).__init__()
        self.arg = arg


class ServicesView(APIView):
    """
        View class for managing of account's services via REST
    """
    def get_object(self, id):
        try:
            return Services.objects.get(id=id)
        except Services.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        logger.debug('ServicesView get')

        if ('account' in request.GET):
            # return active service for curent accoutn
            service = Services.objects.get(account=request.GET.get('account'))
            serializer = ServicesSerializer(service, many=False)
            return Response(serializer.data)

        elif ('id' in request.GET):
            # return service by id
            service = Services.objects.get(id=request.GET.get('id'))
            serializer = ServicesSerializer(service, many=False)
            return Response(serializer.data)

        else:
            #return all active services
            services = Services.objects.filter(is_active=True)
            serializer = ServicesSerializer(services, many=True)
            return Response(serializer.data)

    def post(self, request):
        logger.debug('ServicesView post ------')
        logger.debug( request.POST )

        if 'id' in request.POST:
            # update
            service = self.get_object(request.POST.get('id'))
            if service:
                serializer = ServicesSerializer(service, data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug('----- new ------')
            # 100 new account
            serializer = ServicesSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        # fail
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


############################################################
def add_account(request):
    logger.debug("add_account")

    saving_result = {'success': 1,}

    if request.method == 'POST':
        form = AccountShortModelForm(request.POST)
        try:
            if (form.is_valid() == True):
                new_account = form.save()
                new_account.save()
            else:
                logger.error("ERROR: add_account account is not valid" + json.dumps(request.POST))
                saving_result['success'] = 0

        except (Exception) as ex:
            logger.error("ERROR: add_account can't add account" + json.dumps(request.POST))
            logger.error(ex)
            saving_result['success'] = 0

    else:
        saving_result['success'] = 0

    return HttpResponse(json.dumps(saving_result), content_type="application/json")

def get_accounts_for_page(request, page=1):
    logger.debug("get_accounts_for_page:" + str(page))
    page_count = Accounts.objects.values('porch').distinct().count()
    service_form = ServiceModelForm()
    logger.debug(str(service_form).replace('<input', '\n\n<input'))
    data = {
        'account_form': AccountShortModelForm(),
        'service_form': ServiceModelForm(),
        'pages': range(1, page_count + 1),
        'current_page': page,
    }

    return render_to_response('html/accounts_view.html', RequestContext(request, data))

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)