# parse_np_sequencing_runs


Nanopore data when saved by minknow comes with a number of folders and files. However, for documentation, storage and upload it would be convenient to have a slightly different structure. For our purpose we have decided that the data should go in a folder with a unique `<runID>`. This `<runID>` consists of `<yyyymmdd>_np_<FLOWcellID>` to make it easy to spot the data that was generated using nanopore technology.

## Desired data structure:
Keeping only the pass reads.

`<runID>/`
- `fastq/`
  - `<runID>_<barcode>_<basecaller_version>_<basecalling_model>.fastq.gz`
- `fast5/`
  - `<runID>_<barcode>.tar.gz`
- `pod5/`
  - `<runID>_<barcode>.tar.gz`
- `reports/`
  - all the reports (html, json, rmd. tsv, csv, etc.) 
- `metadata.txt`

## Default structure from minknow
`/<run_name>/<run_name>/<yyyymmdd>_<hhmm>_<position>_<FLOWcellID>_<somehexcode>/`

- `fastq_pass/`
  - `barcode01/`
    - `<FLOWcellID>_pass_barcode01_<somehexcode>_<somehexcode>_<file_number>.fastq.gz`
- `fastq_fail/`
  - `barcode01/`
    - `<FLOWcellID>_fail_barcode01_<somehexcode>_<somehexcode>_<file_number>.fastq.gz`
- `fast5_pass/`
  - `barcode01/`
    - `<FLOWcellID>_pass_barcode01_<somehexcode>_<somehexcode>_<file_number>.fast5`
- `fast5_fail/`
  - `barcode01/`
    - `<FLOWcellID>_fail_barcode01_<somehexcode>_<somehexcode>_<file_number>.fast5`
- `other_reports/`
  - `pore_scan_data_<FLOWcellID>_<somenumber>_<somehexcode>.csv`  
  - `temperature_adjust_data_<FLOWcellID>_<somenumber>_<somehexcode>.csv` 
- `report_<FLOWcellID>_<yyyymmdd>_<hhmm>_<somenumber>.html`
- `report_<FLOWcellID>_<yyyymmdd>_<hhmm>_<somenumber>.json`
- `report_<FLOWcellID>_<yyyymmdd>_<hhmm>_<somenumber>.md`
- `sample_sheet_<FLOWcellID>_<yyyymmdd>_<hhmm>_<somenumber>.csv`
- `throughput_<FLOWcellID>_<somenumber>_<somehexcode>.csv`
- `sequencing_summary_<FLOWcellID>_<somenumber>_<somehexcode>.txt`
- `final_summary_<FLOWcellID>_<somenumber>_<somehexcode>.txt`
- `barcode_alignment__<FLOWcellID>_<somenumber>_<somehexcode>.tsv`
- `pore_activity_<FLOWcellID>_<somenumber>_<somehexcode>.csv`


## Solution

- Get fastq files `python concat_fastqgzfiles.py {inputdir} {outputdir}`
- Get fast5 files processed `python tar_fast5.py {inputdir} {outputdir}`
- Get reports collected `python move_reports.py {inputdir} {outputdir}`
