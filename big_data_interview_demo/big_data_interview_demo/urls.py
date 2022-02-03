"""big_data_interview_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from django.views import static 
from django.conf import settings 
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    url(r'^media/(?P<path>.*)$', static.serve,{'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
    path(r'__hiddenadmin/', admin.site.urls),
    path(r'member/', include('membersystem.urls'), name='member'),
    path(r'popular_content/', include('popular_content.urls'), name='popular_content'),
    
    path('get_token/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get_token/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


schema_view = get_schema_view(
   openapi.Info(
      title="Big Data API",
      default_version='v1',
      description="Big Data",
   ),
    public=True,
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', login_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    url(r'^swagger/$', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    url(r'^redoc/$', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
    url(r'^accounts/', include('rest_framework.urls', namespace='rest_framework'))
]

