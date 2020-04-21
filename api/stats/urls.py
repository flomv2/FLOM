from django.urls import path, include
from . import views
from rest_framework import routers

dayRouter = routers.DefaultRouter()
dayRouter.register('days', views.getDaysInfo)

monthRouter = routers.DefaultRouter()
monthRouter.register('months', views.getMonthsInfo)

yearRouter = routers.DefaultRouter()
yearRouter.register('years', views.getYearsInfo)

urlpatterns = [
    path('days/', include(dayRouter.urls)),
    path('months/', include(monthRouter.urls)),
    path('years/', include(yearRouter.urls))
]