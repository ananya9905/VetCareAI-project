from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    owner = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'pets'
    )
    
    name = models.CharField(max_length = 100)
    species = models.CharField(
        max_length = 20,
        choices= SPECIES_CHOICES
    )
    
    breed = models.CharField(
        max_length= 100,
        blank= True
    )
    
    gender = models.CharField(
        max_length= 10,
        choices= GENDER_CHOICES
    )
    
    date_of_birth = models.DateField(
        null= True,
        blank= True
    )
    
    weight = models.DecimalField(
        max_digits= 6 ,
        decimal_places= 2,
        null= True,
        blank= True
    )
    
    photo = models.ImageField(
        upload_to= 'pet_photos/',
        null= True,
        blank= True
    )
    
    notes = models.TextField(
        blank = True
    )
    
    created_at = models.DateTimeField(
        auto_now_add= True
    )
    
    def __str__(self):
        return self.name

class Vaccination(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete= models.CASCADE,
        related_name= 'vaccinations'
    )
    
    vaccine_name = models.CharField(
        max_length= 100
    )
    
    date_given = models.DateField()
    
    next_due_date = models.DateField(
        null= True,
        blank= True
    )
    
    veterinarian = models.CharField(
        max_length= 150,
        blank= True
    )
    
    notes = models.TextField(
        blank= True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    def __str__(self):
        return f"{self.pet.name} - {self.vaccine_name}"

class MedicalRecord(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    
    record_date = models.DateField()
    diagnosis = models.CharField(
        max_length= 200
    )
    
    symptoms = models.TextField(
        blank= True
    )
    
    treatment = models.TextField(
        blank= True
    )
    
    veterinarian = models.CharField(
        max_length= 150,
        blank = True
    )
    
    notes = models.TextField(
        blank = True
    )
    
    created_at = models.DateTimeField(
        auto_now_add= True
    )
    
    def __str__(self):
        return f"{self.pet.name} - {self.diagnosis}"
    
class Prescription(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete= models.CASCADE,
        related_name= 'prescriptions'
    )
    
    medicine_name = models.CharField(
        max_length= 150
    )
    
    dosage = models.CharField(
        max_length= 100
    )
    
    frequency = models.CharField(
        max_length= 100
    )
    
    duration = models.CharField(
        max_length= 100
    )
    
    prescribed_date = models.DateField()
    
    veterinarian = models.CharField(
        max_length= 150,
        blank = True 
    )
    
    instructions = models.TextField(
        blank = True
    )
    
    created_at = models.DateTimeField(
        auto_now_add= True 
    )
    
    def __str__(self):
        return f"{self.pet.name} - {self.medicine_name}"
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    veterinarian = models.CharField(
        max_length= 150
    )
    
    clinic = models.CharField(
        max_length= 200,
        blank = True
    )
    
    reason = models.TextField(
        blank = True
    )
    
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'scheduled'
    )
    
    notes = models.TextField(
        blank = True
    )
    
    created_at = models.DateTimeField(
        auto_now_add = True
    )
    
    def __str__(self):
        return f"{self.pet.name} - {self.appointment_date}"