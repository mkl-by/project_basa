from django.urls import path, include
from post import views

urlpatterns = [path('', views.Boott, name='boott'),
               path('select', views.Select_val, name='select_val'),
               path('select1', views.SS, name='SS')
               ]
