from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^stuff', views.message, name="message"),    
    url(r'^favorite', views.favorite, name="favorite"),    
    url(r'^logout', views.logout, name="logout"),    
    url(r'^', views.index, name="dashboard"),

]
