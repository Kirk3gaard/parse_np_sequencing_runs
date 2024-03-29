import subprocess
import os
import json
import sys
import glob
import argparse

parser = argparse.ArgumentParser(description='Description of script1')
parser.add_argument('input_dir', type=str, help='Input dir path')
parser.add_argument('output_dir', type=str, help='Output dir path')
args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

#input_dir = "test_data/2023-01-24_np_PAM69896/"
#output_dir = "out_put/"

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