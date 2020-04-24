from django.urls import path
from . import views

urlpatterns = [
	path('',views.index, name="index"),
	# path("stats/days/<floor>/<ID>/<month>", views.getDaysInfo, name = "Days"),
	# path("stats/months/<floor>/<ID>/<year>", views.getMonthsInfo, name = "Months"),
	# path("stats/years/<floor>/<ID>", views.getYearsInfo, name = "Years")
]

views.startThread()
