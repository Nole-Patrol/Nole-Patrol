import os
import re

# Variable to store the directory if user chooses to set it once
global_directory = None


def set_directory():
    global global_directory
    global_directory = input("Please enter the directory path: ")
    if not os.path.exists(global_directory):
        print("Directory does not exist. Falling back to asking for directory for each choice.")
        global_directory = None


def get_directory():
    global global_directory
    if global_directory:
        return global_directory

    while True:
        directory = input("Please enter the directory path: ")
        if os.path.exists(directory):
            return directory
        else:
            print("Directory does not exist. Please enter again.")


def menu():
    print("\n------------------------\n     Database Entry\n------------------------\n" +
          "1. Parse Databases\n" +
          "2. Combine Files\n" +
          "3. Extract FSU Emails (Single File)\n" +
          "4. Extract FSU Emails (Directory)\n" +
          "5. Remove Duplicate Entries (Directory)\n" +
          "6. Remove Invalid Entries (Directory)\n" +
          "7. Fix format of lines\n" +
          "8. Display Stats\n" +
          "9. Display record names and lines\n" +
          "10. Search Data\n" +
          "11. Quit\n")


# Handle Choices - Depending on user input, handle their choice
def handle_choice(choice):
    # 1. Parse Databases
    if choice == "1":
        print("This option will parse a single database and put the data in the correct format")
        input_file = input("Enter input file path: ")
        if not os.path.exists(input_file):
            print("Input file does not exist.")
            return

        parse_databases(input_file)
        print("\033[92mDatabase successfully parsed\033[0m")

    # 2. Combine Files
    elif choice == "2":
        print("This option will combine files if the database is split up in multiple files")
        input_file = input("Enter input file path: ")
        if not os.path.exists(input_file):
            print("Input file does not exist.")
            return

        combine_files_in_directory(input_file)
        print(
            "\033[92mFiles combined and saved to:\033[0m {}".format(os.path.join(input_file, 'combined_data.txt')))

    # 3. Extract Emails (Single File)
    elif choice == "3":
        print("This option will find all fsu.edu matches in a single file and save them")
        input_file = input("Enter input file path: ")
        if not os.path.exists(input_file):
            print("Input file does not exist.")
            return

        total_matches = search_matches(input_file)
        print("\033[92mTotal matches found: {}\033[0m".format(total_matches))

    # 4. Extract Emails (Directory)
    elif choice == "4":
        print("This option will find all fsu.edu matches in multiple files and save them")
        directory_path = get_directory()
        if not os.path.exists(directory_path):
            print("Directory does not exist.")
            return

        # Prompt the user for the output folder
        output_folder = input("Enter the output folder path to store matches: ")
        if not os.path.exists(output_folder):
            print("Output folder does not exist.")
            return

        total_matches = search_matches_multiple(directory_path, output_folder)
        print("\033[92mTotal matches found: {}\033[0m".format(total_matches))

    # 5. Remove Duplicate Entries (Directory)
    elif choice == "5":
        print("This option will remove duplicate lines found in files")
        directory_path = get_directory()
        if not os.path.exists(directory_path):
            print("Directory does not exist.")
            return

        duplicate_lines = remove_duplicate_lines(directory_path)
        print("\033[91mTotal duplicate lines removed:\033[0m {}".format(duplicate_lines))

    # 6. Remove Entries with Errors (Directory)
    elif choice == "6":
        print("This option will remove lines with errors or not in the Email:Password format")
        directory_path = get_directory()
        if not os.path.exists(directory_path):
            print("Directory does not exist.")
            return

        error_matches = remove_errors(directory_path)
        print("\033[91mTotal lines with errors removed:\033[0m {}".format(error_matches))
        print(
            "\033[92mLines with errors saved to:\033[0m {}".format(os.path.join(directory_path, 'errors.txt')))

    # 10. Fix Semicolon Format (Directory)
    elif choice == "7":
        print("This option will fix the semicolon format (email;password) in multiple files")
        directory_path = get_directory()
        if not os.path.exists(directory_path):
            print("Directory does not exist.")
            return

        fix_semicolon_format_in_files(directory_path)
        print("\033[92mSemicolon format fixed in files.\033[0m")
    # 7. Display Stats
    elif choice == "8":
        print("This option displays statistics from all databases")
        directory_path = get_directory()
        if not os.path.exists(directory_path):
            print("Directory does not exist.")
            return

        display_stats(directory_path)

    # 8. Display record names and lines
    elif choice == "9":
        print("This option will save a list of record names and amount of lines (For use in Excel)")
        directory_path = get_directory()
        if not os.path.exists(directory_path):
            print("Directory does not exist.")
            return

        record_lines_names(directory_path)

    # 9. Search data
    elif choice == "10":
        print("This option will search the data and print email matches")
        directory_path = get_directory()
        if not os.path.exists(directory_path):
            print("Directory does not exist.")
            return

        search_data(directory_path)


# Parse Databases - Parses a given database when it's in not correct format
def parse_databases(input_file):
    # Many databases are in different formats, and one function won't be able to work for all of them
    # This inner function needs adjustments based on the database format

    # Format Lines - Extracts and formats the relevant information from a line in the database
    def format_line(data_line):
        parts = data_line.strip().split(':')
        if len(parts) >= 4:
            return f"{parts[1]}:{parts[2]}"
        else:
            return None

    # Determine the output file name based on the input file name

    # Split input file name and its extension
    base_name, ext = os.path.splitext(input_file)

    # Construct the name for the output file
    output_file = base_name + "_parsed" + ext

    # Open the input file for reading and the output file for writing
    with (open(input_file, 'r', encoding="iso-8859-1")
          as infile, open(output_file, 'w', encoding="iso-8859-1") as outfile):

        for line in infile:
            # Format the current line using the inner function
            formatted_line = format_line(line)

            # If the line is successfully formatted, write it to the output file
            if formatted_line:
                outfile.write(formatted_line + '\n')

    # Print a message indicating where the parsed data is saved
    print(f"Formatted data saved to {output_file}")


# Combine files - Combines separate files (Used when a database is split up)
def combine_files_in_directory(directory_path):
    # Generate the path for the output file
    output_file_path = os.path.join(directory_path, "combined_data.txt")

    # Open the output file for writing
    with open(output_file_path, 'w', encoding='iso-8859-1') as output_file:
        # Iterate through all files in the directory and its subdirectories
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                # Skip processing the output file itself
                if file_name == "combined_data.txt":
                    continue

                # Construct the full path to the current file
                file_path = os.path.join(root, file_name)

                try:
                    # Open the current file for reading
                    with open(file_path, 'r', encoding='iso-8859-1') as input_file:
                        for line in input_file:
                            # Remove any extra whitespace
                            line = line.strip()

                            # Write the processed line to the output file
                            output_file.write(line + '\n')

                # Handle any errors that arise while reading the file
                except (IOError, UnicodeDecodeError) as e:
                    print(f"Error reading file '{file_path}': {e}")


# Search matches (One file) - Searches for matches for fsu.edu in databases
def search_matches(input_file_path):
    # Define the search patterns keywords
    keywords = [r"@fsu\.edu", r"@[a-zA-Z]+\.(fsu\.edu)"]

    # Initialize counter for matched lines
    line_count = 0

    # Determine the base name and extension of the input file
    base_name, ext = os.path.splitext(input_file_path)

    # Construct the name for the output file based on the input file's name
    output_file_path = base_name + "_matches" + ext

    # Open the output file for writing
    with open(output_file_path, "w", encoding="iso-8859-1") as output_file:
        try:
            # Open the input file for reading
            with open(input_file_path, "r", encoding="iso-8859-1", errors="ignore") as input_file:
                for line in input_file:
                    for keyword in keywords:
                        # Check if the current line matches any of the keywords
                        match = re.search(keyword, line)

                        if match:
                            # Write the matched line to the output file
                            output_file.write(f"{line}")
                            line_count += 1

                            # Exit the inner loop after a match to avoid duplicate entries
                            break

        # Handle any errors that arise while processing the file
        except Exception as e:
            print(f"Error processing {input_file_path}: {str(e)}")

    # Return the total count of matched lines
    return line_count


# Modify the search_matches_multiple function to accept an output_folder argument
def search_matches_multiple(directory_path, output_folder):
    # Define the search patterns keywords
    keywords = [r"@fsu\.edu", r"@[a-zA-Z]+\.(fsu\.edu)"]

    # Initialize counter for matched lines
    line_count = 0

    # Iterate through all files in the directory and its subdirectories
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            # Construct the full path to the current file
            file_path = os.path.join(root, file_name)

            # List to store lines that match the keywords
            matches = []

            try:
                # Open the current file for reading
                with open(file_path, "r", encoding="iso-8859-1", errors="ignore") as input_file:
                    for line in input_file:
                        for keyword in keywords:
                            # Check if the current line matches any of the keywords
                            match = re.search(keyword, line)
                            if match:
                                # Add the matched line to the matches list
                                matches.append(line)
                                line_count += 1

                                # Exit the inner loop after a match to avoid duplicate entries
                                break

            # Handle any errors that arise while processing the file
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

            # If any matches were found in the current file
            if matches:
                # Construct the name for the output file based on the original file's name
                output_file_path = os.path.join(output_folder, f"{file_name}_matches.txt")

                # Open the output file for writing and save the matched lines
                with open(output_file_path, "w", encoding="iso-8859-1") as output_file:
                    output_file.writelines(matches)

    return line_count


# Remove Duplicates - Goes through all files to remove duplicate lines.
def remove_duplicate_lines(directory_path):
    # Total number of duplicates
    total_duplicates = 0

    # Open a file to write duplicates
    duplicates_file_path = os.path.join(directory_path, "duplicates.txt")
    with open(duplicates_file_path, "w", encoding="iso-8859-1") as duplicates_file:

        # Walk through the directory and its subdirectories
        for dirpath, _, filenames in os.walk(directory_path):
            for filename in filenames:
                # Skip processing desktop.ini files and the duplicates file itself
                if filename.lower() in ["desktop.ini", "duplicates.txt"]:
                    continue

                # Construct the full path to the current file
                file_path = os.path.join(dirpath, filename)

                try:
                    # Open the current file for reading
                    with open(file_path, "r", encoding="iso-8859-1") as input_file:
                        lines = input_file.readlines()

                    # Use a dictionary to track unique lines
                    unique_lines = {}

                    # List to store non-duplicate lines
                    output_lines = []

                    # Iterate through each line in the file
                    for line in lines:
                        # Normalize the line to a consistent case for comparison
                        line_lower = line.lower()

                        # Check if the lowercase version of the line hasn't been seen before
                        if line_lower not in unique_lines:
                            # Add the original line to the output list
                            output_lines.append(line)
                            # Mark the lowercase line as seen
                            unique_lines[line_lower] = True
                        else:
                            # Since it's a duplicate, write it to the duplicates file
                            duplicates_file.write(line)

                    # Calculate the number of duplicate lines removed
                    num_duplicates = len(lines) - len(output_lines)
                    total_duplicates += num_duplicates

                    # Write the non-duplicate lines back to the original file
                    with open(file_path, "w", encoding="iso-8859-1") as output_file:
                        output_file.writelines(output_lines)

                # Handle any errors that arise while processing the file
                except Exception as e:
                    print(f"An error occurred processing {file_path}: {str(e)}")

    # Print the total number of duplicates removed
    print(f"Total duplicates removed: {total_duplicates}")
    print(f"Check '{duplicates_file_path}' for the list of duplicates.")

    return total_duplicates


def remove_errors(directory_path):
    # Expression for valid lines
    valid_pattern = re.compile(r'^[^:]+:[^:]+$')

    # Total number of errors and the invalid lines
    total_errors = 0
    erroneous_lines = []

    # Walk through the directory
    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in filenames:
            # Skip processing desktop.ini files
            if filename == "desktop.ini":
                continue

            file_path = os.path.join(foldername, filename)

            # Read and process each file
            try:
                with open(file_path, 'r', encoding="iso-8859-1") as file:
                    lines = file.readlines()
            except Exception as e:
                print(f"Error reading file {file_path}: {str(e)}")
                continue

            # Filter out invalid lines and keep track of them
            valid_lines = []
            for line in lines:
                stripped_line = line.strip()
                if valid_pattern.match(stripped_line):
                    valid_lines.append(stripped_line + "\n")
                else:
                    total_errors += 1
                    # Replace ";" with ":" and add to erroneous lines
                    corrected_line = stripped_line.replace(";", ":")
                    erroneous_lines.append(corrected_line + "\n")

            # Write back only valid lines to the file
            try:
                with open(file_path, 'w', encoding="iso-8859-1") as file:
                    file.writelines(valid_lines)
            except Exception as e:
                print(f"Error writing to file {file_path}: {str(e)}")
                continue

    # Write erroneous lines to a new errors file
    try:
        with open(os.path.join(directory_path, 'errors.txt'), 'w', encoding="iso-8859-1") as err_file:
            err_file.writelines(erroneous_lines)
    except Exception as e:
        print(f"Error writing to errors.txt: {str(e)}")

    return total_errors


def fix_semicolon_format_in_files(directory_path):
    # Walk through the directory
    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in filenames:
            # Skip processing desktop.ini files
            if filename == "desktop.ini":
                continue

            file_path = os.path.join(foldername, filename)

            # Read and process each file
            try:
                with open(file_path, 'r', encoding="iso-8859-1") as file:
                    lines = file.readlines()
            except Exception as e:
                print(f"Error reading file {file_path}: {str(e)}")
                continue

            # Replace ";" with ":" in each line if the format is "email;password"
            updated_lines = []
            for line in lines:
                stripped_line = line.strip()
                if ";" in stripped_line:
                    parts = stripped_line.split(";")
                    if len(parts) == 2:
                        corrected_line = f"{parts[0]}:{parts[1]}\n"
                        updated_lines.append(corrected_line)
                    else:
                        updated_lines.append(stripped_line + "\n")
                else:
                    updated_lines.append(stripped_line + "\n")

            # Write back the updated lines to the file
            try:
                with open(file_path, 'w', encoding="iso-8859-1") as file:
                    file.writelines(updated_lines)
            except Exception as e:
                print(f"Error writing to file {file_path}: {str(e)}")
                continue


# Display Statistics - total number of email records, unique emails, and the top 10 domain handles
def display_stats(directory_path):
    # Initialize data structures for storing unique emails and counts for each domain handle
    unique_emails = set()
    domain_handles = {}
    total_records = 0  # Counter for the total number of email records processed

    # Iterate through all files in the directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            # Construct the full path to the current file
            filepath = os.path.join(dirpath, filename)

            # Open the current file for reading
            with open(filepath, 'r', encoding="iso-8859-1") as f:
                for line in f:
                    # Extract email and domain handle using regex
                    match = re.search(r'(\S+)@(\S+):', line)
                    if match:
                        # Normalize the email and domain to lowercase
                        email, domain = map(str.lower, match.groups())

                        # Track the unique email addresses
                        unique_emails.add(email)

                        # Update the domain handle counts
                        if domain in domain_handles:
                            domain_handles[domain] += 1
                        else:
                            domain_handles[domain] = 1

                        # Increment the total records for each matched email
                        total_records += 1

    # Display the gathered statistics
    print("\033[92m\nTotal Records:\033[0m", total_records)
    print("\033[93mUnique Emails:\033[0m", len(unique_emails))
    print("\033[95m\nTop 10 Domain Handles:\033[0m")

    # Sort domain handles by count and display the top 10
    for domain, count in sorted(domain_handles.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"@{domain}: {count}")


# Record Lines & Names - Outputs all the breach names and records (For use in Excel)
def record_lines_names(directory):
    # Lists to store breach names (without extension) and their record counts
    file_names = []
    record_counts = []

    # Walk through the directory
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            # Extract filename without extension
            file_name_without_ext = os.path.splitext(filename)[0]
            file_names.append(file_name_without_ext)

            # Count the number of lines (records) in the file
            with open(file_path, 'r', encoding="iso-8859-1") as file:
                record_count = sum(1 for line in file)
                record_counts.append(record_count)

    # Create output file
    output_file_path = os.path.join(directory, "output.txt")
    with open(output_file_path, 'w', encoding="iso-8859-1") as output_file:
        output_file.write("Breach Names:\n")
        for name in file_names:
            output_file.write(name + "\n")

        output_file.write("\nRecords:\n")
        for count in record_counts:
            output_file.write(str(count) + "\n")

    print("\033[92mOutput saved to {}\033[0m".format(output_file_path))


def search_data(directory):
    # Prompt user for email input
    email_to_search = input("Please enter the email address: ")

    # Normalize the email search term to lowercase
    user_part, domain_part = email_to_search.lower().split('@')

    # Modify the domain regex to allow any subdomain variations and make it case-insensitive
    domain_regex = (
            rf"([a-zA-Z0-9_.+-]+@)?([a-zA-Z0-9-]+\.)?"
            + re.escape(domain_part.split('.')[-2])
            + r"\."
            + re.escape(domain_part.split('.')[-1])
    )

    # Compile the regex pattern to search for variations of the email domain
    email_regex = re.compile(domain_regex, re.IGNORECASE)

    # Counter to track the number of entries found
    entry_count = 0

    # Walk through the directory
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            # Open the file and search for the email
            with open(file_path, 'r', encoding="iso-8859-1") as file:
                for line in file:
                    try:
                        # Use the regex to search within the line
                        match = email_regex.search(line)
                        if match:
                            # Extract email and password
                            email, password = line.strip().split(":")

                            if email.lower().startswith(user_part.lower() + "@"):
                                # Extract filename without extension
                                file_name_without_ext = os.path.splitext(filename)[0]

                                # Display the results
                                print("\033[91m\nEmail:\033[0m {}".format(email))
                                print("\033[91mPassword:\033[0m {}".format(password))
                                print("\033[93mBreach:\033[0m {}".format(file_name_without_ext))

                                # Increment entry counter
                                entry_count += 1
                    except ValueError:
                        continue

    # Display "Total Entries:" with the count in red
    print("\n\033[91mTotal Entries:\033[0m {}".format(entry_count))


def main():
    valid_choices = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    choice = ""

    # Prompt user to set a directory at the start
    set_directory_choice = input("Do you want to set a directory once? (yes/no): ").lower().strip()
    if set_directory_choice == "yes":
        set_directory()

    while choice != "11":
        menu()
        choice = input("Choose an option (1-10): ")

        # Check if choice is valid
        if choice not in valid_choices:
            print("Invalid choice. Valid options: (1-10)")
            continue

        # If valid, handle the choice
        try:
            handle_choice(choice)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            continue

    print("Exiting program...")


if __name__ == "__main__":
    main()
