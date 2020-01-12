from django.urls import path
from . import views
from postproc import views

urlpatterns = [
    path('', views.PostProcView.as_view(), name='postproc'),
    path('', views.postProcHtml, name='postProcHtml')
]
