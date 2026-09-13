from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import date, timedelta

from .forms import PetOwnerRegistrationForm
from .models import UserProfile
from pets.models import Pet

def register_owner(request):
    
    if request.method == 'POST':
        form = PetOwnerRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            UserProfile.objects.create(
                user = user,
                role = 'owner'
            )
            return redirect('login')
    else:
        form = PetOwnerRegistrationForm()
    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request, 
            username = username,
            password = password
        )
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(
                request,
                'accounts/login.html',
                {'error': 'Invalid username or password.'}
            )
    return render(
        request,
        'accounts/login.html'
    )

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    pets = Pet.objects.filter(
        owner = request.user
    )
    
    today = date.today()
    reminder_date = today + timedelta(days = 30)
    
    vaccination_reminders = []
    
    for pet in pets:
        vaccinations = pet.vaccinations.all()
        for vaccination in vaccinations:
            if vaccination.next_due_date:
                if vaccination.next_due_date < today:
                    vaccination.status = 'overdue'
                    vaccination_reminders.append(
                        (pet, vaccination)
                    )
                elif vaccination.next_due_date <= reminder_date:
                    vaccination.status = 'upcoming'
                    vaccination_reminders.append(
                        (pet, vaccination)
                    )
    
    return render(
        request, 
        'accounts/dashboard.html',
        {
            'vaccination_reminder': vaccination_reminders
        }
    )
    
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')
# Create your views here.
