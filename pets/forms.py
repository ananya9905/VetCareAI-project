from django import forms
from .models import Pet, Vaccination, MedicalRecord, Prescription, Appointment

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name',
            'species',
            'breed',
            'gender',
            'date_of_birth',
            'weight',
            'photo',
            'notes',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs = {'type': 'date'}
            ),
            
            'notes': forms.Textarea(
                attrs = {
                    'rows': 4,
                    'placeholder': 'Enter any additional information...'
                }
            ),
        }
        
class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        
        fields = [
            'vaccine_name',
            'date_given',
            'next_due_date',
            'veterinarian',
            'notes',
        ]
        
        widgets = {
            'date_given': forms.DateInput(
                attrs= {'type': 'date'}
            ),
            'next_due_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter any additional information...'
                }
            ),
        }
        
class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            'record_date',
            'diagnosis',
            'symptoms',
            'treatment',
            'veterinarian',
            'notes',
        ]
        widgets = {
            'record_date': forms.DateInput(
                attrs = {'type': 'date'}
            ),
            
            'symptoms': forms.Textarea(
                attrs= {
                    'rows': 4,
                    'placeholder' : 'Describe the symptoms...'
                }
            ),
            
            'treatment': forms.Textarea(
                attrs= {
                    'rows': 4,
                    'placeholder': 'Describe the treatment...'
                }
            ),
            
            'notes': forms.Textarea(
                attrs= {
                    'rows': 4,
                    'placeholder': 'Additional notes...'
                }
            ),
        }
        
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        
        fields = [
            'medicine_name',
            'dosage',
            'frequency',
            'duration',
            'prescribed_date',
            'veterinarian',
            'instructions',
        ]
        
        widgets = {
            'prescribed_date': forms.DateInput(
                attrs= {'type': 'date'}
            ),
            
            'instructions': forms.Textarea(
                attrs= {
                    'rows': 4,
                    'placeholder': 'Enter medicine instructions...'
                }
            ),
        }
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'appointment_date',
            'appointment_time',
            'veterinarian',
            'clinic',
            'reason',
            'status',
            'notes',
        ]
        widgets = {
            'appointment_date': forms.DateInput(
                attrs = {'type': 'date'}
            ),
            'appointment_time': forms.TimeInput(
                attrs = {'type': 'time'}
            ),
            'reason': forms.Textarea(
                attrs = {'rows': 3}
            ),
            'notes': forms.Textarea(
                attrs = {'rows': 3}
            ),
        }