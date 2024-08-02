import os
import json

# Define the paths
json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../db/Base.json')
root_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../components')

# List of prohibited symbols in Windows filenames
prohibited_symbols = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']

# Function to read JSON data
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(f"JSON data read from {file_path}")
    return data

# Function to check for prohibited symbols in a string
def contains_prohibited_symbols(name):
    for symbol in prohibited_symbols:
        if symbol in name:
            print(f"SYMBOL {symbol} CAN'T BE USED IN FILENAME! Rename the component: {name}")
            return True
    return False

# Function to create folder structure
def create_folder_structure(data, root_path):
    created_folders = 0
    skipped_folders = 0
    prohibited_symbol_folders = 0

    for item in data:
        site_category = item['siteCategory']
        technical_category = item['technicalCategory']
        name = item['name']

        # Check for prohibited symbols in the name
        if contains_prohibited_symbols(name):
            prohibited_symbol_folders += 1
            continue

        folder_name = f"id{item['id']}_v{item['version']}_{name}"

        # Construct the full path
        full_path = os.path.join(root_path, site_category, technical_category, folder_name)
        print_path = os.path.join(site_category, technical_category, folder_name)

        # Create the folders if they don't exist
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            created_folders += 1
            print(f"Created folder: {print_path}")
        else:
            skipped_folders += 1
            print(f"Skipped existing folder: {print_path}")

    return created_folders, skipped_folders, prohibited_symbol_folders

# Main function to control the flow
def main():
    # Read the JSON data
    data = read_json(json_file_path)

    # Create the folder structure
    created_folders, skipped_folders, prohibited_symbol_folders = create_folder_structure(data, root_folder_path)

    # Print summary
    print(f"Total folders to be created: {len(data)}")
    print(f"Folders created: {created_folders}")
    print(f"Folders skipped: {skipped_folders}")
    print(f"Folders with prohibited symbols: {prohibited_symbol_folders}")

    # Pause the script to keep the console window open
    input("Press Enter to exit...")

# Run the main function
if __name__ == "__main__":
    main()