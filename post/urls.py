from django.urls import path, include, re_path
from post import views


urlpatterns = [path('', views.Boott, name='boott'),
               path('select', views.Select_val, name='select_val'),
               path('select1', views.SS, name='SS'),
               path('vedomost', views.VedomNal, name='vedom_nal'),
               re_path(r'^data_input/(?P<idd>\d+)/$', views.Data_input, name='data_input'),
               re_path(r'^data_input/0/(?P<idd>\d+)/$', views.Form_input.as_view(), name='form_input'),
               ]
