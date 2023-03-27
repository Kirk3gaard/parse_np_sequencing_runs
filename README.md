# parse_np_sequencing_runs


Nanopore data when saved by minknow comes with a number of folders and files. However, for documentation, storage and upload it would be convenient to have a slightly different structure. 

## desired data structure:

`runID/`
- `fastq/`
  - `runID_barcode_basecaller version_basecalling model.fastq.gz`
- `fast5/`
  - `runID_barcode.tar.gz`
- `pod5/`
  - `runID_barcode.tar.gz`
- `reports/`
- `metadata.txt`

## Default structure from minknow
- `fastq_pass/`
  - `barcode01/`
    - `barcode01....fastq`
- `fastq_fail/`
  - `barcode01/`
    - `barcode01....fastq`
- `fast5_pass/`
  - `barcode01/`
    - `barcode01....fastq`
- `fast5_fail/`
  - `barcode01/`
    - `barcode01....fastq`
- `other_reports/`
- `report_<>.html`
- `report_<>.json`
- `report_<>.md`
- `sample_sheet_<>.csv`
- `throughput_PAG71663_12795670_c9425df7.csv`
- `sequencing_summary_PAG71663_12795670_c9425df7.txt`
- `final_summary_PAG71663_12795670_c9425df7.txt`
- `barcode_alignment_PAG71663_12795670_c9425df7.tsv`
- `pore_activity_PAG71663_12795670_c9425df7.csv`


