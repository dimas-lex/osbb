import os
import sys
sys.path.append('/home/yana/code/osb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'osb.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
