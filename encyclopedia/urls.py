from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
    path('wiki/create/', views.create, name='create'),
    path('wiki/edit/<str:title>/', views.edit, name='edit'),
    path('wiki/random', views.random_entry, name='random'),
    path('wiki/<str:title>', views.single_entry, name='single-entry'),

    path("", views.index, name="index"),
]
