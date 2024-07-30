import os
# Этот скрипт считывает имена файлов из двух текстов
# и переименовывает все файлы в указанной директории, подставляя соответствующие имена из текстовых файлов.

import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the files and the directory
from_file_path = os.path.join(script_dir, 'from.txt')
to_file_path = os.path.join(script_dir, 'to.txt')
directory_path = os.path.join(script_dir, '../cropwhite/to_crop')

# Read the filenames from the files
with open(from_file_path, 'r', encoding='utf-8') as from_file:
    from_filenames = from_file.read().splitlines()

with open(to_file_path, 'r', encoding='utf-8') as to_file:
    to_filenames = to_file.read().splitlines()

# Check if the number of filenames match
if len(from_filenames) != len(to_filenames):
    raise ValueError("The number of filenames in from.txt and to.txt do not match")

# Rename the files
for from_name, to_name in zip(from_filenames, to_filenames):
    from_path = os.path.join(directory_path, from_name)
    to_path = os.path.join(directory_path, to_name)
    
    if os.path.exists(from_path):
        os.rename(from_path, to_path)
        print(f'Renamed: {from_name} to {to_name}')
    else:
        print(f'File not found: {from_name}')