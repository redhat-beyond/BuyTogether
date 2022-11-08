"""
<<<<<<< HEAD
<<<<<<< HEAD
WSGI config for BuyTogether project.
=======
WSGI config for buy_together project.
>>>>>>> d00f754 (Adding a Django development environment)
=======
WSGI config for buy_together project.
>>>>>>> d00f754 (Adding a Django development environment)

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buy_together.settings')

application = get_wsgi_application()
