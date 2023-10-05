import os
import re


def menu():
    print("------------------------\n     Database Entry\n------------------------\n" +
          "1. Parse Databases\n" +
          "2. Combine Files\n" +
          "3. Extract Emails (Single File)\n" +
          "4. Extract Emails (Directory)\n" +
          "5. Omit Duplicate Entries (Directory)\n" +
          "6. Display Stats\n" +
          "7. Quit\n")


def handle_choice(choice):
    if choice == "1":
        input_file = input("Enter input file path: ")
        if not os.path.exists(input_file):
            print("Input file does not exist.")
            return

        parse_databases(input_file)

    elif choice == "2":
        input_directory = input("Enter input directory path: ")
        if not os.path.exists(input_directory):
            print("Input directory does not exist.")
            return

        combine_files_in_directory(input_directory)
        print(f"Files combined and saved to {os.path.join(input_directory, 'combined_data.txt')}")

    elif choice == "3":
        input_file = input("Enter input file path: ")
        if not os.path.exists(input_file):
            print("Input file does not exist.")
            return

        total_matches = search_matches(input_file)
        print(f"Total matches found: {total_matches}")

    elif choice == "4":
        root_dir = input("Enter root directory path: ")
        if not os.path.exists(root_dir):
            print("Directory does not exist.")
            return

        search_matches_multiple(root_dir)
        print("Search completed and match files created.")

    elif choice == "5":
        directory_path = input("Enter the directory path: ")
        if not os.path.exists(directory_path):
            print("Directory does not exist.")
            return

        remove_duplicate_lines(directory_path)

    elif choice == "6":
        input_file_path = input("Enter folder path that holds the data: ")
        if not os.path.exists(input_file_path):
            print("Folder does not exist.")
            return

        display_stats(input_file_path)


def parse_databases(input_file):
    """
    This parses a given database when it's in not correct format
    Many databases are in different formats, and one function won't be able to work for all of them
    This inner function needs adjustments based on the database format
    """

    def format_line(line):
        """
        Extracts and formats the relevant information from a line in the database

        line: A line from the input file.
        return: Formatted line or None if the line doesn't meet the criteria
        """
        parts = line.strip().split(':')
        if len(parts) >= 4:
            return f"{parts[1]}:{parts[2]}"
        else:
            return None

    # Automatically determine the output file name based on the input file name
    base_name, ext = os.path.splitext(input_file)  # Split input file name and its extension
    output_file = base_name + "_parsed" + ext  # Construct the name for the output file

    # Open the input file for reading and the output file for writing
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Format the current line using the inner function
            formatted_line = format_line(line)
            if formatted_line:  # If the line is successfully formatted, write it to the output file
                outfile.write(formatted_line + '\n')

    # Print a message indicating where the parsed data is saved
    print(f"Formatted data saved to {output_file}")


def combine_files_in_directory(directory_path):
    """
    Combines the contents of all files in a directory into a single output file named "combined_data.txt"

    directory_path: Path to the directory containing files
    """

    # Generate the path for the output file within the provided directory
    output_file_path = os.path.join(directory_path, "combined_data.txt")

    # Open the output file for writing
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Iterate through all files in the directory and its subdirectories
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                # Skip processing the output file itself to avoid recursive inclusion
                if file_name == "combined_data.txt":
                    continue

                # Construct the full path to the current file
                file_path = os.path.join(root, file_name)

                try:
                    # Open the current file for reading
                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        for line in input_file:
                            # Remove any extra whitespace
                            line = line.strip()
                            # Write the processed line to the output file
                            output_file.write(line + '\n')
                except (IOError, UnicodeDecodeError) as e:
                    # Handle any errors that arise while reading the file
                    print(f"Error reading file '{file_path}': {e}")


def search_matches(input_file_path):
    """
    Searches for specific patterns (keywords) in the given file and writes matched lines to a new output file

    input_file_path: Path to the file to be searched
    return: Number of lines that matched any of the keywords
    """

    # Define the search patterns (keywords) we're looking for within the file
    keywords = [r"@fsu\.edu", r"@[a-zA-Z]+\.(fsu\.edu)"]

    line_count = 0  # Initialize counter for matched lines

    # Determine the base name and extension of the input file
    base_name, ext = os.path.splitext(input_file_path)

    # Construct the name for the output file based on the input file's name
    output_file_path = base_name + "_matches" + ext

    # Open the output file for writing
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        try:
            # Open the input file for reading
            with open(input_file_path, "r", encoding="utf-8", errors="ignore") as input_file:
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
        except Exception as e:
            # Handle any errors that arise while processing the file
            print(f"Error processing {input_file_path}: {str(e)}")

    # Return the total count of matched lines
    return line_count


def search_matches_multiple(directory_path):
    """
    Searches for specific patterns (keywords) in all files within the given directory
    For each file, if any lines match the patterns, those lines are written to a new output file

    directory_path: Path to the directory containing files to be searched
    """

    # Define the search patterns (keywords) we're looking for within the files
    keywords = [r"@fsu\.edu", r"@[a-zA-Z]+\.(fsu\.edu)"]

    # Iterate through all files in the directory and its subdirectories
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            # Construct the full path to the current file
            file_path = os.path.join(root, file_name)
            matches = []  # List to store lines that match the keywords

            try:
                # Open the current file for reading
                with open(file_path, "r", encoding="utf-8", errors="ignore") as input_file:
                    for line in input_file:
                        for keyword in keywords:
                            # Check if the current line matches any of the keywords
                            match = re.search(keyword, line)
                            if match:
                                # Add the matched line to the matches list
                                matches.append(line)
                                # Exit the inner loop after a match to avoid duplicate entries
                                break
            except Exception as e:
                # Handle any errors that arise while processing the file
                print(f"Error processing {file_path}: {str(e)}")

            # If any matches were found in the current file
            if matches:
                # Construct the name for the output file based on the original file's name
                output_file_path = os.path.join(root, f"{file_name}_matches.txt")
                # Open the output file for writing and save the matched lines
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.writelines(matches)


def remove_duplicate_lines(directory_path):
    """
    Iterates through all files in the given directory to remove duplicate lines.

    directory_path: Path to the directory containing files to be processed
    """

    # Walk through the directory and its subdirectories
    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            # Construct the full path to the current file
            file_path = os.path.join(dirpath, filename)

            try:
                # Open the current file for reading
                with open(file_path, "r", encoding="iso-8859-1") as input_file:
                    lines = input_file.readlines()

                # Use a set to track unique lines for efficient look-up
                unique_lines = set()
                output_lines = []  # List to store non-duplicate lines

                # Iterate through each line in the file
                for line in lines:
                    # Check if the line hasn't been seen before
                    if line not in unique_lines:
                        # Add the unique line to the output list
                        output_lines.append(line)
                        # Mark the line as seen
                        unique_lines.add(line)

                # Write the non-duplicate lines back to the original file
                with open(file_path, "w", encoding="iso-8859-1") as output_file:
                    output_file.writelines(output_lines)

                # Calculate and print the number of duplicate lines removed
                removed_lines = len(lines) - len(output_lines)
                if removed_lines > 0:
                    print(f"In file {file_path}, total removed lines: {removed_lines}")

            except Exception as e:
                # Handle any errors that arise while processing the file
                print(f"An error occurred processing {file_path}: {str(e)}")


def display_stats(directory_path):
    """
    Statistics include the total number of email records, the count of unique emails, and the top 10 domain handles

    directory_path: Path to the directory containing files to be analyzed.
    """

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
            with open(filepath, 'r', encoding="utf-8") as f:
                for line in f:
                    # Extract email and domain handle using regex
                    match = re.search(r'(\S+)@(\S+):', line)
                    if match:
                        email, domain = match.groups()
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
    print("Total Records Found:", total_records)
    print("Unique Emails:", len(unique_emails))
    print("\nTop 10 Domain Handles:")
    # Sort domain handles by count and display the top 10
    for domain, count in sorted(domain_handles.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"@{domain}: {count}")


def main():
    valid_choices = ["1", "2", "3", "4", "5", "6", "7"]
    choice = ""

    while choice != "7":
        menu()
        choice = input("Choose an option (1-7): ")

        # Check if the user's choice is valid
        if choice not in valid_choices:
            print("Invalid choice. Valid options: (1-7)")
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
