from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^processreg$', views.processreg),
    url(r'^processlog$', views.processlog),
    url(r'^success$', views.success),
]