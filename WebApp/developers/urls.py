from django.urls import path
from . import views

'''
This will find the corresponding view 
named "index"
'''
urlpatterns = [
	path('',views.index, name="index"),
]
