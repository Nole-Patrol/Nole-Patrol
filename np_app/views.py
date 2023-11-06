'''
Description: This file contains the code for the views of the np_app.
Author(s): Michael Sousa, Brian Arango, Caitlin Marie Grimes
Last Modified Date: 27 October 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/topics/http/views/
            https://docs.djangoproject.com/en/4.2/ref/request-response/
'''
import os
from django.shortcuts import render
from .forms import EmailSearchForm, PasswordGeneratorForm
from .models import EmailFile, RegisteredUser
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
import string
import random

'''
Function Name: index(request)
Description: This function contains the code to render the index.html page and
             process the user's email search query.
Parameters: request
Return Value: HTTPResponse
Author(s): Michael Sousa Jr., Caitlin Marie Grimes
Last Modified Date: 27 October 2023
Assumptions: N/A
References: https://docs.djangoproject.com/en/4.2/ref/request-response/
'''
def index(request):
    print("Request method:", request.method)  # Debugging statement
    
    # Create instances of the forms
    email_form = EmailSearchForm(request.POST or None)
    password_form = PasswordGeneratorForm(request.POST or None)
    
    generated_password = None  # Default to no password generated

    if request.method == 'POST': 
        # Check if the email search form was submitted
        if 'email' in request.POST and email_form.is_valid():
            user_email = email_form.cleaned_data['email']
            print("User email:", user_email)  # Debugging statement
            
            # Use Django's ORM to search for the email in the database.
            matching_records = EmailFile.objects.filter(name=user_email)
            print("Matching records:", matching_records)  # Debugging statement
            
            # If the email is found in the database, extract the distinct sources.
            if matching_records.exists():
                sources = set(record.source for record in matching_records)
                # Render the search.html page with the results.
                return render(request, 'search.html', {'user_email': user_email, 'sources': sources})
            else: 
                print("No matching records for:", user_email)  # Debugging statement
                # Render the search.html page with the no_match flag set to True.
                return render(request, 'search.html', {'no_match': True})
        
        # Check if the password generator form was submitted
        elif 'generate_password' in request.POST and password_form.is_valid():
            # Generate a password if the button was clicked
            generated_password = generate_password()
        
        else:
            print("Form errors:", email_form.errors)  # Debugging statement
    
    # Render the index.html page with the forms and the generated password (if any)
    return render(request, 'index.html', {
        'email_form': email_form,
        'password_form': password_form,
        'generated_password': generated_password
    })
            
def breaches_page(request):
    return render(request, 'breaches.html')
            
def about_page(request):
    return render(request, 'about.html')

'''
Function Name: notify_page(request)
Description: This function handles the process of notifying users if their email is found in the breached 
             database. On a POST request, it checks the EmailFile model for the provided email. If found,
             it sends a breach notification to the user's email. Additionally, the email is saved in the
             RegisteredUser model if not already present. After processing, it redirects to a success page.
             It also sends a thank you email as a confirmation, useful for testing purposes.
Parameters: request
Return Value: HTTPResponse
Author(s): Brian Arango
Last Modified Date: 30 October 2023
Assumptions: The EmailFile model contains emails from breached databases. The RegisteredUser model saves 
             users who have been notified.
References: https://docs.djangoproject.com/en/4.2/ref/request-response/, 
            https://docs.djangoproject.com/en/4.2/topics/email/#
'''
def notify_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if the email exists in the EmailFile model.
        exists_in_breach = EmailFile.objects.filter(name=email).exists()
        
        # If it exists in the breach, send a notification email to the user.
        breach_message = 'Your email has been found in our database of breached emails.\n' + \
                         'For a full list of past breaches affecting your email address, ' + \
                         'please see our database. We will notify you if your email is found in any future breaches.'
        if exists_in_breach:
            send_mail(
                'Breach Notification',
                breach_message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        
        # Save the email in the RegisteredUser model if it's not already there.
        created = RegisteredUser.objects.get_or_create(email=email)
        
        # If the user is newly registered (i.e., email was just added), send a thank you email.
        if created:
            send_mail(
                'Thank you for registering for Nole Patrol breach notifications',
                'Thank you for registering for email breach notifications. We will notify you if your email is found in any future breaches.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        
        # Redirect to a success page or display a success message (based on your design).
        return HttpResponseRedirect('/success/')  # Change this URL based on your design.

    return render(request, 'notify.html')
 
def success_view(request):
    return render(request, 'success.html')

'''
Function Name: generate_password(length=12)
Description: This function generates a random password of the specified length.
Parameters: length
Return Value: password
Author(s): Brian Arango
Last Modified Date: 3 November 2023
'''
# Password generation function
def generate_password(length=12, include_lowercase=True, include_uppercase=True, include_numbers=True, include_special=True):
    characters = ''
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for i in range(length)) if characters else ''
    return password
