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
from .forms import EmailSearchForm
from .models import EmailFile

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
    
    if request.method == 'POST': 
        form = EmailSearchForm(request.POST)
        
        if form.is_valid():
            user_email = form.cleaned_data['email']
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
        else:
            print("Form errors:", form.errors)  # Debugging statement

    else: 
        form = EmailSearchForm()
    
    return render(request, 'index.html', {'form': form})
            
def breaches_page(request):
    return render(request, 'breaches.html')
            
def about_page(request):
    return render(request, 'about.html')

def notify_page(request):
    return render(request, 'notify.html')
 

#commented out search fnx for now (focusing on UI/UX) -michael
    """
    if request.method == 'POST': 
        form = EmailSearchForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            matching_files = []

            #iterate throught .txt files in "email" folder
            for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), 'emails')):
                for file in files: 
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            lines = f.read().splitlines()
                            for line in lines:
                                #split the line by ":" and take email 
                                parts = line.split(':', 1)
                                if len(parts) > 0:
                                    email_part = parts[0]
                                else:
                                    #incase theres no ":"
                                    email_part = line

                                if user_email == email_part:
                                    matching_files.append(os.path.basename(file_path))

                            #emails = f.read().splitlines()
                            #if user_email in emails: 
                            #    matching_files.append(os.path.basename(file_path))

            if matching_files:
                return render(request, 'search.html', {'user_email': user_email, 'matching_files': matching_files})
            else: 
                return render(request, 'search.html', {'no_match': True})

    else: 
        form = EmailSearchForm()
    
    return render(request, 'index.html', {'form': form})

    """
