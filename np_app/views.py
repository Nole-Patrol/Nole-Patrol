import os
from django.shortcuts import render
from .forms import EmailSearchForm
from .models import EmailFile

def index(request):
    return render(request, 'index.html')
            
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
