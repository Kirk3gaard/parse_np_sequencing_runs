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
# define the maximum size of each tar.gz file
max_size = 500 * 1024 * 1024 * 1024  # 500 GB

# Locate json file and the fast5_pass directory
json_files = []
# Loop through all directories and files in the specified directory
for root, dirs, files in os.walk(input_dir):
    for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    # Check if the "fast5_pass" directory is in the list of directories
    if "fast5_pass" in dirs:
        # If it is, save the path to the "fastq_pass" directory to a variable
        fast5_pass_dir = os.path.join(root, "fast5_pass")
        break

# Load the JSON data from the report file
with open(json_files[0], 'r') as f:
    data = json.load(f)

# Access the value of "guppy_filename" field
guppy_filename = data['protocol_run_info']['args']
for arg in guppy_filename:
    if arg.startswith('--guppy_filename='):
        guppy_filename_value = arg.split('=')[1].replace(".cfg", "")
        break            

# Access the version of guppy
guppy_version = data['software_versions']['guppy_connected_version']        

# Access the  flowcell ID
flow_cell_id = data['protocol_run_info']['flow_cell']['flow_cell_id']    

# Access the  flowcell ID
start_time_value = data['protocol_run_info']['start_time'].split("T")[0]    
        
# Define the variables to check
variables_to_check = [json_files, fast5_pass_dir, guppy_filename_value, guppy_version, flow_cell_id, start_time_value]

# Loop over the variables and check if they are defined
for variable in variables_to_check:
    try:
        print(variable)
    except NameError:
        print(f"The '{variable}' was not found.")

# Create runid        
runid_val = f'{start_time_value}_np_{flow_cell_id}'

# Prepare folder structure
fast5_output_dir = f'{output_dir}/fast5'
if os.path.exists(f'{fast5_output_dir}'):
    print(f'The folder {fast5_output_dir} exists.')
else:
    print(f'The folder {fast5_output_dir} does not exist.')
    os.mkdir(f'{fast5_output_dir}')


######################
# Define function
######################
import os
import subprocess

def tar_files(input_dir, output_dir, prefix):
    # Get a list of all the files in the input directory
    file_list = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    
    # Sort the file list by size
    file_list.sort(key=lambda f: os.path.getsize(f))
    print(file_list)
    # Split the files into separate groups based on the maximum size limit
    max_size = 500 * 1024 * 1024 * 1024 # 500 GB in bytes
    split_files = []
    current_size = 0
    current_files = []
    for f in file_list:
        f_size = os.path.getsize(f)
        if current_size + f_size > max_size:
            split_files.append(current_files)
            current_size = 0
            current_files = []
        current_files.append(f)
        current_size += f_size
    if current_files:
        split_files.append(current_files)
    #print(split_files)
    # Tar each group of files and save the resulting tar.gz file to the output directory
    for i, files in enumerate(split_files):
        output_file = os.path.join(output_dir, prefix + '_' + str(i) + '.tar.gz')
        command = f'tar -cvf {output_file} {" ".join(str(x) for x in files)}'
        #print(command)
        subprocess.run(command, shell=True)



######################

# Check if barcodes have been used 
fast5_files = glob.glob(os.path.join(fast5_pass_dir, "*fast5"))
if fast5_files:
    print("fast5 files found in the directory")
    tar_files(f'{fast5_pass_dir}', f'{fast5_output_dir}', f'{runid_val}.')

# Generate all the barcode combinations
barcodes = [f'barcode{i:02d}' for i in range(1, 97)] + ['unclassified']   # Replace with your barcode sequences
# Check if a barcode folder exists and concatenate the content of each barcode folder
for barcode in barcodes:
    barcode_dir = os.path.join(fast5_pass_dir, barcode)
    if not os.path.exists(barcode_dir):
        continue  # Skip if there are no files for this barcode
    input_files = os.listdir(barcode_dir)
    if not input_files:
        continue  # Skip if there are no reads for this barcode
    print(barcode)
    tar_files(f'{barcode_dir}', f'{fast5_output_dir}', f'{runid_val}.{barcode}')

        
