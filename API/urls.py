
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('login', views.login),
    re_path('carreras/add/', views.add_carrera),
    re_path('api/carreras/', views.list_carreras),
    path('api/list_carreras/<int:id>/', views.get_carrera, name='get-carrera'),
    path('api/update_carreras/<int:id>/', views.update_carrera, name='update-carrera'),
    path('api/delete_carreras/<int:id>/', views.delete_carrera, name='delete-carrera'),
    re_path('api/alumnos/', views.list_alumnos),
    path('api/list_alumnos/<int:id>/', views.get_alumno, name='get-alumno'),
    path('api/update_alumnos/<int:id>/', views.update_alumno, name='update-alumno'),
    path('api/delete_alumnos/<int:id>/', views.delete_alumno, name='delete-alumno'),
    re_path('alumnos/add/', views.add_alumno),
]