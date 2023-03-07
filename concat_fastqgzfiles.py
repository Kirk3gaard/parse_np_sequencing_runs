import subprocess
import os
import json
import sys
import glob

input_dir = "test_data/2022-12-22_np_PAG65826/"
output_dir = "out_put/"

# json file
json_files = []

# Loop through all directories and files in the specified directory
for root, dirs, files in os.walk(input_dir):
    for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    # Check if the "fastq_pass" directory is in the list of directories
    if "fastq_pass" in dirs:
        # If it is, save the path to the "fastq_pass" directory to a variable
        fastq_pass_dir = os.path.join(root, "fastq_pass")
        break

# Load the JSON data from a file
with open(json_files[0], 'r') as f:
    data = json.load(f)

# Access the value of "guppy_filename" field
guppy_filename = data['protocol_run_info']['args']
for arg in guppy_filename:
    if arg.startswith('--guppy_filename='):
        guppy_filename_value = arg.split('=')[1]
        break            

guppy_version = data['software_versions']['guppy_connected_version']        
        
# Check if the variable is defined
try:
    print(json_files)
except NameError:
    print("The 'json_file' was not found in the specified directory.")

# Check if the variable is defined
try:
    print(fastq_pass_dir)
except NameError:
    print("The 'fastq_pass' directory was not found in the specified directory.")

# Check if the variable is defined
try:
    print(guppy_filename_value)
except NameError:
    print("The 'guppy_filename_value' field was not located.")

# Check if the variable is defined
try:
    print(guppy_version)
except NameError:
    print("The 'guppy_version' was not found.")

# 
barcodes = [f'barcode{i:02d}' for i in range(1, 97)] + ['unclassified']  # Replace with your barcode sequences
#
for barcode in barcodes:
    barcode_dir = os.path.join(fastq_pass_dir, barcode)
    if not os.path.exists(barcode_dir):
        continue  # Skip if there are no files for this barcode
    
    input_files = os.listdir(barcode_dir)
    if not input_files:
        continue  # Skip if there are no reads for this barcode
    
    output_file = os.path.join(output_dir, f'{barcode}.{guppy_filename_value}.fastq.gz')
    command = f'cat {barcode_dir}/*.fastq.gz > {output_file}'
    print(command)
    subprocess.run(command, shell=True)
