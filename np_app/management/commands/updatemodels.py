'''
Description: This file contains the code to import data from .txt files into the
             EmailFile model. The data is imported from the following directories:
                np_app/Database/data/ComboLists
                np_app/Database/data/Database Dumps
                np_app/Database/data/databases
            The data is imported into the EmailFile model and associated SQLite 
            database using Django's bulk_create() method to improve performance.
            The password data is encrypted using the encrypt_password() method 
            from the EmailFile model. The progress bar is implemented using the
            pyprog module. The time module is used to calculate the time it 
            takes to import the data.
Author(s): Sarah Zeidan, Caitlin Marie Grimes
Last Modified Date: 1 November 2023
Assumptions: For records to be successfully inserted into the database, we 
             assume the data is in the correct format (email:password), that 
             the data is in the correct directories, and that the data is not
             already in the database.
References: https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/
'''
import os
import time
import pyprog
from django.core.management.base import BaseCommand
from np_app.models import EmailFile

start_time = time.time()

'''
Class Name: Command(BaseCommand)
Description: This class inherits from Django's BaseCommand class and contains
             the code to import data from .txt files into the EmailFile model
             and the associated SQLite database.
Author(s): Sarah Zeidan, Caitlin Marie Grimes
Last Modified Date: 1 November 2023
Assumptions: For records to be successfully inserted into the database, we 
             assume the data is in the correct format (email:password), that 
             the data is in the correct directories, and that the data is not
             already in the database.
References: https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/
'''
class Command(BaseCommand):
    
    '''
    Function Name: handle(self, *args, **options)
    Description: This function contains the code to import data from .txt files
                 into the EmailFile model and the associated SQLite database,
                 excluding duplicates.
    Parameters: self, *args, **options
    Return Value: N/A
    Author(s): Sarah Zeidan, Brian Arango, Caitlin Marie Grimes
    Last Modified Date: 27 October 2023
    Assumptions: For records to be successfully inserted into the database, we 
                 assume the data is in the correct format (email:password) and that 
                 the data is in the correct directories.
    References: https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/
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
        format_error_counter = 0
        format_error_lines = []
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
                            # Create an instance of the EmailFile model
                            email_file_instance = EmailFile(name=email, source=file_name_without_extension)
                            # Encrypt the password using the set_password method from the EmailFile model
                            email_file_instance.set_password(password)
                            # Append the instance to the email_instances list.
                            email_instances.append(email_file_instance)
                        else:
                            format_error_counter += 1
                            format_error_lines.append(line)

                    except UnicodeDecodeError:
                        self.stdout.write(self.style.ERROR(f'UnicodeDecodeError in file: {file_path}'))
        
        new_email_instances = []
        record_count = EmailFile.objects.all().count()
        # If the EmailFile model is empty, bulk insert instances into the EmailFile model and SQLite database.
        if record_count == 0:
            EmailFile.objects.bulk_create(email_instances)
            # Informative outputs.
            self.stdout.write('\n')
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(email_instances)} entries.'))
            if format_error_counter:
                self.stdout.write(self.style.ERROR(f'Skipped {format_error_counter} lines due to incompatible formatting.'))
                # Print to file the lines that were skipped due to incompatible formatting.
                with open('format_error_lines.txt', 'w') as file:
                    for line in format_error_lines:
                        file.write(line)
        # If the EmailFile model is not empty, check for duplicates and skip them.
        else:
            skipped_lines_counter = 0
            for instance in email_instances:
                if EmailFile(name=instance.name, password=instance.password, source=instance.source):
                    skipped_lines_counter += 1
                else:
                    new_email_instances.append(instance)
            # Bulk insert new instances into the EmailFile model and SQLite database.
            EmailFile.objects.bulk_create(new_email_instances)
            # Informative outputs.
            self.stdout.write('\n')
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(new_email_instances)} entries.'))
            if skipped_lines_counter:
                self.stdout.write(self.style.ERROR(f'Skipped {skipped_lines_counter} duplicates.'))
            if format_error_counter:
                self.stdout.write(self.style.ERROR(f'Skipped {format_error_counter} lines due to incompatible formatting.'))
                # Print to file the lines that were skipped due to incompatible formatting.
                with open('np_app/management/commands/emailfile_insert_errors.txt', 'w') as file:
                    for line in format_error_lines:
                        file.write(line)

        prog.end()

        # Print error message if no data has been imported into the EmailFile model.
        #if EmailFile.objects.exists() == False:
        #    self.stdout.write(self.style.ERROR('No data has been imported into the EmailFile model.'))

        print(time.time() - start_time, "seconds")