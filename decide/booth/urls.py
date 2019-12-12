from django.urls import path, include
from .views import BoothView


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('i18n/', include('django.conf.urls.i18n')),
]
