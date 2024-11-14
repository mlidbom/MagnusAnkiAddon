import shutil
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the source directory (venv) and target directory (project) relative to the script location
source_dir = os.path.join(script_dir, './venv/lib/site-packages')
target_dir = os.path.join(script_dir, './src/MagnusAddon/_lib')

# One line per library and its dependencies
libraries_to_copy = [
    'wanikani_api', 'dateutil', 'six.py',
    'janome',
    'pyperclip',
    'beartype',
    'jamdict', 'jamdict_data', 'puchikarui', 'chirptext',
    'unidic2ud', 'fugashi', 'ufal', #Not sure about this line, was not added when it should have been.
    'ginza', 'ja_ginza', 'ja_ginza-5.1.3.dist-info', 'spacy', 'spacy-3.6.1.dist-info', 'spacy_legacy-3.0.12.dist-info', 'spacy_loggers-1.0.5.dist-info', 'spacy_legacy', 'spacy_loggers', 'thinc', 'numpy', 'numpy.libs', 'catalogue', 'sudachipy', 'sudachidict_core', 'confection', 'srsly', 'pydantic', 'pydantic_core', 'typing_extensions.py', 'annotated_types', 'wasabi', 'blis', 'cymem', 'preshed', 'murmurhash', 'langcodes', 'tqdm', 'typer'
    ]

# Create the target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Copy the libraries
for library in libraries_to_copy:
    source_path = os.path.join(source_dir, library)
    target_path = os.path.join(target_dir, library)

    is_dir = os.path.isdir(source_path)

    # Remove the existing directory if it exists
    if os.path.exists(target_path):
        shutil.rmtree(target_path) if is_dir else os.remove(target_path)

    # Copy the directory
    shutil.copytree(source_path, target_path) if is_dir else shutil.copy2(source_path, target_path)

print("Libraries copied successfully!")
