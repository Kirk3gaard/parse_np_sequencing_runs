import subprocess
import os
from pathlib import Path
import json
import argparse
import glob

# Function to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Description of script1')
    parser.add_argument('input_dir', type=str, help='Input dir path')
    parser.add_argument('output_dir', type=str, help='Output dir path')
    return parser.parse_args()

# Function to locate the pod5_pass directory and JSON files
def locate_pod5_pass_and_json_files(input_dir):
    json_files = []

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))

        if "pod5_pass" in dirs:
            pod5_pass_dir = os.path.join(root, "pod5_pass")
            break

    return json_files, pod5_pass_dir

# Function to load JSON data and extract required information
def load_and_extract_data(json_files):
    with open(json_files[0], 'r') as f:
        data = json.load(f)

    guppy_filename = data['protocol_run_info']['args']
    for arg in guppy_filename:
        if arg.startswith('--guppy_filename='):
            guppy_filename_value = arg.split('=')[1].replace(".cfg", "")
            break

    guppy_version = data['software_versions']['guppy_connected_version']
    flow_cell_id = data['protocol_run_info']['flow_cell']['flow_cell_id']
    start_time_value = data['protocol_run_info']['start_time'].split("T")[0]

    return guppy_filename_value, guppy_version, flow_cell_id, start_time_value

# Function to check if the required variables are defined
def check_variables(variables_to_check):
    for variable in variables_to_check:
        try:
            print(variable)
        except NameError:
            print(f"The '{variable}' was not found.")

# Function to create a run ID
def create_runid(start_time_value, flow_cell_id):
    return f'{start_time_value}_np_{flow_cell_id}'

# Function to prepare the output directory
def prepare_output_dir(output_dir):
    pod5_output_dir = f'{output_dir}/pod5'
    if os.path.exists(f'{pod5_output_dir}'):
        print(f'The folder {pod5_output_dir} exists.')
    else:
        print(f'The folder {pod5_output_dir} does not exist.')
        os.mkdir(f'{pod5_output_dir}')
    
    return pod5_output_dir

# Function to create tar files from input files while ensuring the maximum size constraint
def tar_files(input_dir, output_dir, prefix):
    file_list = sorted([os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))],
                        key=lambda f: os.path.getsize(f))
    max_size = 500 * 1024 * 1024 * 1024
    split_files = []
    current_size = 0
    current_files = []

    # Group files based on the maximum size constraint
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

        # Create tar files from grouped files
    for i, files in enumerate(split_files):
        output_file = os.path.join(output_dir, prefix + '_' + str(i) + '.tar.gz')
        with open(os.path.join(output_dir, f'{prefix}_{i}.txt'), 'w') as f:
            f.write('\n'.join(files))
        command = f'tar -czvf {output_file} --files-from {os.path.join(output_dir, f"{prefix}_{i}.txt")}'
        subprocess.run(command, shell=True)

# Main function
def main():
    args = parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    json_files, pod5_pass_dir = locate_pod5_pass_and_json_files(input_dir)
    guppy_filename_value, guppy_version, flow_cell_id, start_time_value = load_and_extract_data(json_files)
    variables_to_check = [json_files, pod5_pass_dir, guppy_filename_value, guppy_version, flow_cell_id, start_time_value]
    check_variables(variables_to_check)
    runid_val = create_runid(start_time_value, flow_cell_id)
    pod5_output_dir = prepare_output_dir(output_dir)

    pod5_files = glob.glob(os.path.join(pod5_pass_dir, "*pod5"))
    if pod5_files:
        print("pod5 files found in the directory")
        tar_files(pod5_pass_dir, pod5_output_dir, f'{runid_val}.')

    barcodes = [f'barcode{i:02d}' for i in range(1, 97)] + ['unclassified']
    for barcode in barcodes:
        barcode_dir = os.path.join(pod5_pass_dir, barcode)
        if not os.path.exists(barcode_dir):
            continue
        input_files = os.listdir(barcode_dir)
        if not input_files:
            continue
        print(barcode)
        tar_files(barcode_dir, pod5_output_dir, f'{runid_val}.{barcode}')

if __name__ == "__main__":
    main()
