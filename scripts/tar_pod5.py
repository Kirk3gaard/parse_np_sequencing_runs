import subprocess
import os
from pathlib import Path
import json
import argparse
import glob

def parse_args():
    parser = argparse.ArgumentParser(description='Description of script1')
    parser.add_argument('input_dir', type=str, help='Input dir path')
    parser.add_argument('output_dir', type=str, help='Output dir path')
    return parser.parse_args()

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

def check_variables(variables_to_check):
    for variable in variables_to_check:
        try:
            print(variable)
        except NameError:
            print(f"The '{variable}' was not found.")

def create_runid(start_time_value, flow_cell_id):
    return f'{start_time_value}_np_{flow_cell_id}'

def prepare_output_dir(output_dir):
    pod5_output_dir = f'{output_dir}/pod5'
    if os.path.exists(f'{pod5_output_dir}'):
        print(f'The folder {pod5_output_dir} exists.')
    else:
        print(f'The folder {pod5_output_dir} does not exist.')
        os.mkdir(f'{pod5_output_dir}')
    
    return pod5_output_dir

def tar_files(input_dir, output_dir, prefix):
    file_list = sorted([os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))],
                        key=lambda f: os.path.getsize(f))
    max_size = 500 * 1024 * 1024 * 1024
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

    for i, files in enumerate(split_files):
        output_file = os.path.join(output_dir, f'{prefix}_{i}.tar.gz')
        with open(os.path.join(output_dir, f'{prefix}_{i
