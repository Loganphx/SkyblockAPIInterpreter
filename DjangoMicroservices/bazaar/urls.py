from django.urls import path
from . import views

app_name = 'bazaar'

urlpatterns = [
    path('bazaar/get_item_names', views.get_bazaar_item_name, name='REST API get Bazaar names'),
]
