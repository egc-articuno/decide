from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('listCensus', views.list_census, name='listCensus'),
    path('addCensus', views.add_census, name='addCensus'),
    path('saveNewCensus', views.save_new_census, name='saveNewCensus'),
    path('editCensus', views.edit_census, name='editCensus'),
    path('saveEditedCensus', views.save_edited_census, name='saveEditedCensus'),
    path('deleteCensus', views.delete_census, name='deleteCensus'),
    path('deleteSelectedCensus', views.delete_selected_census, name='deleteSelectedCensus'),
    path('exportCensus', views.exportCSV, name='exportCensus'), 
    path('listCensusCP', views.list_census_CP, name='listCensusCP'),
    path('addCensusCP', views.add_census_CP, name='addCensusCP'),
    path('saveNewCensusCP', views.save_new_census_CP, name='saveNewCensusCP')
]
