import subprocess
import os

barcodes = [f'barcode{i:02d}' for i in range(1, 97)] + ['unclassified']  # Replace with your barcode sequences
input_dir = '/user_data/rhk/parse_np_sequencing_runs/test_data/2022-12-22_np_PAG65826/2022-12-22_np_PAG65826/20221222_1539_2G_PAG65826_a9e3e1e7/fastq_pass/'  # Replace with the directory containing all the fastq.gz files
output_dir = '2022_np_out/'  # Replace with the directory where you want to save the concatenated files

for barcode in barcodes:
    barcode_dir = os.path.join(input_dir, barcode)
    if not os.path.exists(barcode_dir):
        continue  # Skip if there are no files for this barcode
    
    input_files = os.listdir(barcode_dir)
    if not input_files:
        continue  # Skip if there are no reads for this barcode
    
    output_file = os.path.join(output_dir, f'{barcode}.fastq.gz')
    command = f'cat {barcode_dir}/*.fastq.gz > {output_file}'
    print(command)
    subprocess.run(command, shell=True)
