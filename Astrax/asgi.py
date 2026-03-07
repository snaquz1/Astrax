"""
ASGI config for Astrax project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
print("🔥 ASGI LOADED 🔥")
from channels.auth import AuthMiddleware, AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import Chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Astrax.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app, #Важно
    "websocket": AuthMiddlewareStack(
        URLRouter(Chat.routing.websocket_urlpatterns)

    ),
})
