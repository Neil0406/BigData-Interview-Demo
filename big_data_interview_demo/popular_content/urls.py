from django.conf.urls import url
from popular_content import views
from django.urls import path

popular_content = views.popular_content

urlpatterns = [
    path('', popular_content),
]
