from django.urls import path
from . import views

urlpatterns = [
    path('pets/', views.my_pets, name = 'my_pets'),
    path('pets/add/', views.add_pet, name = 'add_pet'),
    path('pets/<int:pet_id>/', views.pet_detail, name = 'pet_detail'),
    path('pets/<int:pet_id>/vaccination/add/', views.add_vaccination, name = 'add_vaccination'),
    path('pets/<int:pet_id>/medical-record/add/', views.add_medical_record, name = 'add_medical_record'),
    path('pets/<int:pet_id>/prescription/add', views.add_prescription, name = 'add_prescription'),
    path('pets/<int:pet_id>/appointment/add/', views.add_appointment, name = 'add_appointment'),
    path('appointment/<int:appointment_id>/cancel/', views.cancel_appointment,name = 'cancel_appointment'),
    path('symptom-checker/', views.symptom_checker, name = 'symptom_checker'),
]
