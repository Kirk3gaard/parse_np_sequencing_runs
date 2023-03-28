import json
import sys

# Get the file path from the command line argument
file_path = sys.argv[1]

# Load the JSON data from a file
with open(file_path, 'r') as f:
    data = json.load(f)

# Access the value of "guppy_filename" field
guppy_filename = data['protocol_run_info']['args']
for arg in guppy_filename:
    if arg.startswith('--guppy_filename='):
        guppy_filename_value = arg.split('=')[1]
        break
# Print the value
print(guppy_filename_value)