"""
URL configuration for hotel_hp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView

from hotel.urls import urls as hotel_urls

schema_view = get_schema_view(
   openapi.Info(
      title="Store API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hotel/', include(hotel_urls)),

    path("", TemplateView.as_view(template_name="index.html")),
    path("login", TemplateView.as_view(template_name="login.html")),
    path("logout", LogoutView.as_view()),
    path("accounts/", include("allauth.urls")),

    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
