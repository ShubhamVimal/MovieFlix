from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path("<int:pk>/", views.details, name='details'),
    path("<slug:genre>/", views.allmovies, name='allmovies'),
    path("searchResults", views.searchResults, name='searchResults')

    # path('/',views.index,name='index'),
    # path("/<int:pk>", views.details, name='details'),
    # path("/<slug:genre>", views.allmovies, name='allmovies'),
    # path("/<slug:q>", views.searchResults, name='searchResults')
]