'''
Description: This file contains the code to import data from .txt files into the
             EmailFile model. The data is imported from the following directories:
                np_app/Database/data/ComboLists
                np_app/Database/data/Database Dumps
                np_app/Database/data/databases
            The data is imported into the EmailFile model and associated SQLite 
            database using Django's bulk_create() method to improve performance.
            The data is encrypted using the encrypt_password() method from the 
            EmailFile model. The progress bar is implemented using the pyprog 
            module. The time module is used to calculate the time it takes to
            import the data.
Author(s): Sarah Zeidan, Caitlin Marie Grimes
Last Modified Date: 27 October 2023
Assumptions: For records to be successfully inserted into the database, we 
             assume the data is in the correct format (email:password) and that 
             the data is in the correct directories.
References: N/A
'''
import os
import time
import pyprog # pip install pyprog; see https://pypi.org/project/pyprog/
from django.core.management.base import BaseCommand
from np_app.models import EmailFile

start_time = time.time()

'''
Class Name: Command(BaseCommand)
Description: This class inherits from Django's BaseCommand class and contains
             the code to import data from .txt files into the EmailFile model
             and the associated SQLite database.
Author(s): Sarah Zeidan, Caitlin Marie Grimes
Last Modified Date: 27 October 2023
Assumptions: For records to be successfully inserted into the database, we 
             assume the data is in the correct format (email:password) and that 
             the data is in the correct directories.
References: N/A
'''
class Command(BaseCommand):
    #help = 'Import email data from .txt files in various directories'
    
    '''
    Function Name: handle(self, *args, **options)
    Description: This function contains the code to import data from .txt files
                 into the EmailFile model and the associated SQLite database.
    Parameters: self, *args, **options
    Return Value: N/A
    Author(s): Sarah Zeidan, Brian Arango, Caitlin Marie Grimes
    Last Modified Date: 27 October 2023
    Assumptions: For records to be successfully inserted into the database, we 
                 assume the data is in the correct format (email:password) and that 
                 the data is in the correct directories.
    References: N/A
    '''
    def handle(self, *args, **options):
        data_directories = [
            'np_app/Database/data/ComboLists',
            'np_app/Database/data/Database Dumps',
            'np_app/Database/data/databases',
        ]
        # Get all .txt files in the specified directories and append to file_paths list.
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
        # Print error message if no .txt files are found in the specified directories.
        if not file_paths:
            self.stdout.write(self.style.ERROR('No .txt files found in the specified directories.'))
            return

        # Initialize progress bar.
        prog = pyprog.ProgressBar("", "", len(file_paths))
        prog.update

        email_instances = []
        skipped_lines_counter = 0
        file_counter = 0
        # Iterate through each file in the file_paths list.
        for file_path in file_paths:
            file_counter += 1
            prog.set_stat(file_counter)
            prog.update()

            # Get file name without extension.
            head, tail = os.path.split(file_path)
            file_name = os.path.splitext(tail)
            file_name_without_extension = file_name[0]
            # Open file and iterate through each line.
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    try:
                        # Split each line using ':' as the delimiter.
                        fields = line.strip().split(':')

                        # Check if the line contains both email and password.
                        if len(fields) == 2:
                            email, password = fields
                            # Encrypt the password using the method from the EmailFile model
                            encrypted_password = EmailFile().encrypt_password(password)
                            # Create an instance of the EmailFile model and append to email_instances list.
                            email_instances.append(EmailFile(name=email, password=encrypted_password, source=file_name_without_extension))

                        else:
                            skipped_lines_counter += 1
                    except UnicodeDecodeError:
                        self.stdout.write(self.style.ERROR(f'UnicodeDecodeError in file: {file_path}'))
        # Bulk insert instances into the EmailFile model and SQLite database.
        EmailFile.objects.bulk_create(email_instances)

        # Informative outputs.
        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(email_instances)} entries.'))
        if skipped_lines_counter:
            self.stdout.write(self.style.ERROR(f'Skipped {skipped_lines_counter} lines due to incorrect format.'))

        prog.end()

        # Print error message if no data has been imported into the EmailFile model.
        if EmailFile.objects.exists() == False:
            self.stdout.write(self.style.ERROR('No data has been imported into the EmailFile model.'))

        print(time.time() - start_time, "seconds")