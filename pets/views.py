from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .ai_helper import get_ai_assessment

from .forms import (PetForm, VaccinationForm, MedicalRecordForm, PrescriptionForm, AppointmentForm, )
from .models import Pet, Appointment

@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit= False)
            pet.owner = request.user
            pet.save()
            return redirect('my_pets')
    else:
        form = PetForm()
    return render (
        request,
        'pets/add_pet.html',
        {'form': form}
    )

@login_required
def my_pets(request):
    pets = Pet.objects.filter(
        owner = request.user
    ) 
    return render(
        request,
        'pets/my_pets.html',
        {'pets': pets}
    )
    
@login_required
def pet_detail(request, pet_id):
    pet = Pet.objects.get(
        id = pet_id,
        owner = request.user
    )
    
    vaccinations = pet.vaccinations.all()
    medical_records = pet.medical_records.all()
    prescriptions = pet.prescriptions.all()
    appointments = pet.appointments.all()
    
    return render(
        request,
        'pets/pet_detail.html',
        {
            'pet': pet,
            'vaccinations': vaccinations,
            'medical_records': medical_records,
            'prescriptions': prescriptions,
            'appointments': appointments,
        }
    )

@login_required
def add_vaccination(request, pet_id):
    pet = Pet.objects.get(
        id = pet_id,
        owner = request.user
    )
    
    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            vaccination = form.save(commit = False)
            vaccination.pet = pet
            vaccination.save()
            return redirect(
                'pet_detail',
                pet_id = pet.id
            )
    else:
        form = VaccinationForm()
    return render(
        request,
        'pets/add_vaccination.html',
        {
            'form': form,
            'pet': pet
        }
    )
    
@login_required
def add_medical_record(request, pet_id):
    pet = Pet.objects.get(
        id = pet_id,
        owner = request.user
    )
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit = False)
            medical_record.pet = pet
            medical_record.save()
            return redirect(
                'pet_detail',
                pet_id = pet.id
            )
    else:
        form = MedicalRecordForm()
    return render(
        request,
        'pets/add_medical_record.html',
        {
            'form': form,
            'pet': pet
        }
    )
    
@login_required
def add_prescription(request, pet_id):
    pet = Pet.objects.get(
        id = pet_id,
        owner = request.user
    )
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit = False)
            prescription.pet = pet
            prescription.save()
            return redirect(
                'pet_detail',
                pet_id = pet.id
            )
    else:
        form = PrescriptionForm()
        return render(
            request,
            'pets/add_prescription.html',
            {
                'form': form,
                'pet': pet
            }
        )
        
@login_required
def add_appointment(request, pet_id):
    pet = get_object_or_404(
        Pet,
        id = pet_id,
        owner = request.user
    )
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit = False)
            appointment.pet = pet
            appointment.save()
            
            return redirect('pet_detail', pet_id = pet.id)
    else:
        form = AppointmentForm()
    return render(
        request,
        'pets/add_appointment.html',
        {
            'form': form,
            'pet': pet
        }
    )  
    
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id = appointment_id,
        pet__owner = request.user
    )
    
    appointment.status = 'cancelled'
    appointment.save()
    
    return redirect('pet_detail', pet_id = appointment.pet.id)

@login_required
def symptom_checker(request):
    symptoms = ''
    analysis = ''
    questions = []
    risk_level = ''
    recommendation = ''
    
    if request.method == 'POST':
        
        if request.POST.get('stage') == 'questions':
            raw_symptoms = request.POST.get('symptoms', '').strip()
            symptoms = raw_symptoms
            symptoms_lower = raw_symptoms.lower()
            
            if any(word in symptoms_lower for word in ['vomiting', 'throwing up', 'vomit']):
                analysis = ('Your pet may be experiencing a vomiting-related problem.')
                questions = [
                    'How many times has your pet vomited?',
                    'Is there blood in the vomit?',
                    'Is your pet drinking water normally?',
                    'Is your pet active or very weak?'
                ]
                
            elif any(word in symptoms_lower for word in ['diarrhea', 'loose motion', 'loose stool']):
                analysis = ('Your pet may be experiencing a digestive or diarrhea-related problem.')
                questions = [
                    'How many times has your pet passed loose stool?',
                    'Is there blood or mucus in the stool?',
                    'Is your pet drinking water normally?',
                    'Is your pet active or weak?'
                ]
                
            elif any(word in symptoms_lower for word in ['itching', 'scratching', 'red skin', 'hair loss']):
                analysis = ('Your pet may be experiencing a skin-related problem.')
                questions = [
                    'How long has the itching been present?',
                    'Are there wounds, redness, or hair loss?',
                    'Does your pet have fleas or ticks?',
                    'Is your pet constantly scratching or biting the skin?'
                ]
                
            elif any(word in symptoms_lower for word in ['cough', 'breathing', 'breathless']):
                analysis = ('Your pet may be experiencing a respiratory-related problem.')
                questions = [
                    'Is your pet having difficulty breathing?',
                    'How long has the coughing been present?',
                    'Is there nasal discharge?',
                    'Is your pet weak or unable to walk normally?'
                ]
                
            elif any(word in symptoms_lower for word in ['not eating', 'loss of appetite', 'not drinking']):
                analysis = ('Your pet may be experiencing an appetite or general health problem.')
                questions = [
                    'How long has your pet refused food?',
                    'Is your pet drinking water?',
                    'Is your pet vomiting or having diarrhea?',
                    'Is your pet active or weak?'
                ]
            else:
                analysis = ("More information is needed to understand your pet's symptoms.")
                questions = [
                    'When did the symptoms start?',
                    'Is your pet eating and drinking normally?',
                    'Is your pet active or weak?',
                    'Are the symptoms getting worse?'
                ]
                
            request.session['symptoms'] = raw_symptoms
            request.session['questions'] = questions
            
        elif request.POST.get('stage') == 'assessment':
            symptoms = request.session.get('symptoms', '')
            questions = []
            analysis = 'Your answers have been reviewed.'
            
            answers = []
            
            for key,value in request.POST.items():
                if key.startswith('answer_'):
                    answers.append(value.strip())
            
            combined_text = (symptoms + ' ' + ' '.join(answers)).lower()
            
            emergency_terms = [
                'difficult breathing',
                "can't breath",
                'cannot breath',
                'blue gums',
                'blue tongue',
                'unconscious',
                'severe bleeding',
                'poison',
                'seizure',
                'collapse',
                'collapsed',
                'unable to stand'
            ]
            
            high_risk_terms = [
                'blood in vomit',
                'blood in stool',
                'vomiting blood',
                'bloody vomit',
                'bloody stool',
                'repeated vomiting',
                'very weak',
                'severe pain',
                'swollen abdomen',
                'cannot keep water'
            ]
            
            if any(term in combined_text for term in emergency_terms):
                risk_level = 'Emergency'
                recommendation = (
                    'Seek emergency veterinary care immediately. '
                    'Do not wait for the symptoms to improve.'
                )
            
            elif any(term in combined_text for term in high_risk_terms):
                risk_level = 'High Risk'
                recommendation = ('Contact a veterinarian as soon as possible, preferably today.')
                
            else:
                risk_level = 'Moderate Risk'
                recommendation = ('Arrange a veterinary consultation soon and monitor your pet closely.')
                
            try:
                analysis = get_ai_assessment(symptoms, answers)
            except Exception as e:
                print("AI ERROR:", e)
                analysis = (
                    'The AI assessment is temporarily unavailable. '
                    'Please follow the risk recommendation below.'
                )
                
            request.session.pop('symptoms', None)
            request.session.pop('questions', None)
            
    return render(
        request,
        'pets/symptom_checker.html',
        {
            'symptoms': symptoms,
            'analysis': analysis,
            'questions': questions,
            'risk_level': risk_level,
            'recommendation': recommendation,
        }
    )