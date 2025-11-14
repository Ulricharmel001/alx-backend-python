"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views.
For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema configuration for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Messaging App API",
        default_version='v1',
        description="API documentation for the Messaging App",
        contact=openapi.Contact(email="support@messagingapp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


""""Objective: configure URLS for the conversations and messages

Instructions:

Using Django rest framework DefaultRouter
 to automatically create the conversations and messages for your viewsets

Navigate to the main project’s urls.py i.e messaging_app/urls.py and include your created 
routes with path as api"""
# URL Patterns
 
urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),
    # API routes
    path('api/', include('chats.urls')),
    # default auth route
    path('api-auth/', include('rest_framework.urls')),


    # Swagger documentation routes
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

