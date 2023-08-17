import shutil
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the source directory (venv) and target directory (project) relative to the script location
source_dir = os.path.join(script_dir, './venv/lib/site-packages')
target_dir = os.path.join(script_dir, './src/MagnusAddon/_lib')

# One line per library and its dependencies
libraries_to_copy = ['dateutil',
                     'wanikani_api',
                     'janome',
                     'jamdict', 'jamdict_data', 'puchikarui', 'chirptext']

# Create the target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Copy the libraries
for library in libraries_to_copy:
    src_path = os.path.join(source_dir, library)
    dst_path = os.path.join(target_dir, library)

    # Remove the existing directory if it exists
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)

    # Copy the directory
    shutil.copytree(src_path, dst_path)

print("Libraries copied successfully!")
