from django.urls import path, include
from . import views
from rest_framework import routers

dayRouter = routers.DefaultRouter()
dayRouter.register('', views.daysView)

monthRouter = routers.DefaultRouter()
monthRouter.register('', views.monthsView)

yearRouter = routers.DefaultRouter()
yearRouter.register('', views.yearsView)

urlpatterns = [
    path('days/', include(dayRouter.urls)),
    path('months/', include(monthRouter.urls)),
    path('years/', include(yearRouter.urls))
]