import subprocess
import os

barcodes = ['barcode01', 'barcode02', 'barcode03', 'unbarcoded']  # Replace with your barcode sequences
input_dir = '/path/to/input/'  # Replace with the directory containing all the fastq.gz files
output_dir = '/path/to/output/'  # Replace with the directory where you want to save the concatenated files

for barcode in barcodes:
    barcode_dir = os.path.join(input_dir, barcode)
    if not os.path.exists(barcode_dir):
        continue  # Skip if there are no files for this barcode
    
    input_files = os.listdir(barcode_dir)
    if not input_files:
        continue  # Skip if there are no reads for this barcode
    
    output_file = os.path.join(output_dir, f'{barcode}.fastq.gz')
    command = f'cat {barcode_dir}/*.fastq.gz > {output_file}'
    subprocess.run(command, shell=True)
