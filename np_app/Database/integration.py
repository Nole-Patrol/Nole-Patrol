import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Nole_Patrol.settings")
django.setup()

# Import necessary functionalities from main.py
from main import get_directory

# Import Django models
from your_app_name.models import BreachData

def parse_and_insert_into_django_db():
    directory = get_directory()  # Get directory using the function from main.py

    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.txt'):
                file_path = os.path.join(foldername, filename)
                with open(file_path, 'r', encoding="iso-8859-1") as file:
                    for line in file:
                        if ':' in line:
                            username, password = line.strip().split(":")
                            breach = os.path.splitext(filename)[0]
                            breach_data = BreachData(username=username, password=password, breach=breach)
                            breach_data.save()

if __name__ == "__main__":
    parse_and_insert_into_django_db()