

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat360.settings')

from Text360 import routing

django_asgi_application = get_asgi_application()

application=ProtocolTypeRouter(
    {
        'http': 'django_asgi_application',
        'websocket': AllowedHostsOriginValidator (
            AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
    

        )                                              ,

    }
)


