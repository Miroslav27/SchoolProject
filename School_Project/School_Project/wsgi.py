"""
WSGI config for School_Project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application
path = '/Users/Miroslav/PycharmProjects/Homework4.Django/School_Project'
if path not in sys.path:
    sys.path.append(path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'School_Project.settings')

application = get_wsgi_application()
