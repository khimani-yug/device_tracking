from django.contrib import admin
from django.db import router
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('user', views.userview, basename='user')
router.register('report', views.deviceview, basename='mobile_detail')
router.register('searched', views.searchview, basename='')

urlpatterns = [
    path('registration/',views.registration.as_view()),
    path('login/',views.login.as_view()),
    path('search/',views.search.as_view()),
    path('', include(router.urls)),
]
