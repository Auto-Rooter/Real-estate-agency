from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # The root page,  name=index to easly access this path by giving it a name
    path('about', views.about, name='about'),
]
