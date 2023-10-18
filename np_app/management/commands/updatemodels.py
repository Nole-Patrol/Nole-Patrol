import os
from django.core.management.base import BaseCommand
from np_app.models import EmailFile

class Command(BaseCommand):
    help = 'Import email data from .txt files in various directories'

    def handle(self, *args, **options):
        data_directories = [
            'np_app/Database/data/ComboLists',
            'np_app/Database/data/Database Dumps',
            'np_app/Database/data/databases',
        ]

        file_paths = []
        for directory in data_directories:
            if os.path.isdir(directory):
                if 'ComboLists' in directory or 'databases' in directory:
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            if file.endswith('.txt'):
                                file_paths.append(os.path.join(root, file))
                elif 'Database Dumps' in directory:
                    files = os.listdir(directory)
                    for file in files:
                        if file.endswith('.txt'):
                            file_paths.append(os.path.join(directory, file))

        if not file_paths:
            self.stdout.write(self.style.ERROR('No .txt files found in the specified directories.'))
            return

        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    try:
                        # Split each line using ':' as the delimiter
                        fields = line.strip().split(':')

                        # Check if the line contains both email and password
                        if len(fields) == 2:
                            email, password = fields

                            # Check if the email contains the "@" symbol
                            if "@" in email:
                                source = email.split('@')[1]
                            else:
                                source = "Unknown"  # Handle cases where "@" is missing

                            email_file_instance = EmailFile(name=email, password=password, source=source)
                            email_file_instance.save()

                            self.stdout.write(self.style.SUCCESS(f'Successfully imported: {email_file_instance}'))
                        else:
                            self.stdout.write(self.style.ERROR(f'Skipped line due to incorrect format: {line.strip()}'))
                    except UnicodeDecodeError:
                        self.stdout.write(self.style.ERROR(f'UnicodeDecodeError in file: {file_path}'))

        # Check if any records have been imported into the EmailFile model
        if EmailFile.objects.exists():
            self.stdout.write(self.style.SUCCESS('Data has been imported into the EmailFile model.'))
        else:
            self.stdout.write(self.style.ERROR('No data has been imported into the EmailFile model.'))