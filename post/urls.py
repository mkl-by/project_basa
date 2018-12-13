from django.urls import path, include, re_path
from post import views

"""basa1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

urlpatterns = [path('', views.Boott, name='boott'),
               path('select', views.Select_val, name='select_val'),
               path('basa/registration', views.RegisterFormView.as_view(), name='registration'),
               path('autch', views.LoginFormView.as_view(), name='loginn'),
               # path('registration', views.RegisterFormView.as_view(), name='registration'),

               path('basa/aut', views.LoginFormView.as_view(), name='aut'),
               path('vedomost', views.VedomNal, name='vedom_nal'),
               re_path(r'^data_input/(?P<idd>\d+)/$', views.Data_input, name='data_input'),
               re_path(r'^data_input/0/(?P<idd>\d+)/$', views.Form_input.as_view(), name='form_input'),
               re_path(r'^data_del/(?P<ide>\d+)/$', views.DataDel.as_view(), name='datadel'),
               # path('data_del/', views.DataDel.as_view(), name='datadel'),

               path('d_dell', views.D_dell, name='d_dell'),
               path('select1', views.Select_1, name='select_1'),

               ]
