import subprocess
import os
import json
import sys
import glob

input_dir = "test_data/2022-12-22_np_PAG65826/"
output_dir = "out_put/"

# Locate json file and the fastq_pass directory
json_files = []
# Loop through all directories and files in the specified directory
for root, dirs, files in os.walk(input_dir):
    for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    # Check if the "fastq_pass" directory is in the list of directories
    if "fastq_pass" in dirs:
        # If it is, save the path to the "fastq_pass" directory to a variable
        run_dir = root
        print(root)
        fastq_pass_dir = os.path.join(root, "fastq_pass")
        break

def move_files(input_dir, output_dir, file_extension):
     command = f'cp {input_dir}/*.{file_extension} {output_dir}/'
     subprocess.run(command, shell=True)

# Prepare folder structure
reports_output_dir = f'{output_dir}/reports'
if os.path.exists(f'{reports_output_dir}'):
    print(f'The folder {reports_output_dir} exists.')
else:
    print(f'The folder {reports_output_dir} does not exist.')
    os.mkdir(f'{reports_output_dir}/')

# Define the variables to check
file_extensions = [ 'txt', 'md', 'csv', 'json', 'html', 'tsv']

# Loop over the variables and check if they are defined
for f_ext in file_extensions:
     move_files(f'{run_dir}', f'{reports_output_dir}', f'{f_ext}')