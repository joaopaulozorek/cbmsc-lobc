from django.urls import path
from . import views

urlpatterns = [
	path('', views.bc_list, name='bc_list'),
    #path('', views.post_list, name='post_list'),
]