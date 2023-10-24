import os
from django.shortcuts import render
from .forms import EmailSearchForm
from .models import EmailFile
from django.core.mail import send_mail
from .forms import RegistrationForm
from .forms import VerificationForm
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def index(request):
    print("Request method:", request.method)  # Debugging statement 1
    
    if request.method == 'POST': 
        form = EmailSearchForm(request.POST)
        
        if form.is_valid():
            user_email = form.cleaned_data['email']
            print("User email:", user_email)  # Debugging statement 3

            # Use Django's ORM to search for the email in the EmailFile table
            matching_records = EmailFile.objects.filter(name=user_email)
            print("Matching records:", matching_records)  # Debugging statement 3

            if matching_records.exists():
                return render(request, 'search.html', {'user_email': user_email, 'matching_files': matching_records})
            else: 
                print("No matching records for:", user_email)  # Debugging statement 4
                return render(request, 'search.html', {'no_match': True})
        else:
            print("Form errors:", form.errors)  # Debugging statement 2

    else: 
        form = EmailSearchForm()
    
    return render(request, 'index.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB yet
            user.set_password(form.cleaned_data['password'])
            user.generate_email_verification_token()
            user.save()
            
            # Send verification email
            send_mail(
                'Verify your account',
                f'Your verification token is: {user.email_verification_token}',
                'from_email@example.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('verification_page')  # Redirect to verification page
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def verify(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']

            # Look for a user with the provided token
            user = CustomUser.objects.filter(email_verification_token=token).first()

            if user:
                # Mark the user as email verified
                user.is_email_verified = True
                user.save()

                messages.success(request, 'Your email has been verified. You can now log in.')
                return redirect('login')  # Redirect to the login page
            else:
                messages.error(request, 'Invalid verification token. Please check your email or request a new one.')
        else:
            messages.error(request, 'Invalid token format. Please enter the token exactly as provided.')

    else:
        form = VerificationForm()

    return render(request, 'verify.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('name_of_your_target_view')  # Redirect to a desired URL after login. Replace 'name_of_your_target_view' with your target view's name.
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
