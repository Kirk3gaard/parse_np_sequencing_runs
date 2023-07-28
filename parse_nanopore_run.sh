#!/bin/bash

set -eu

#input1=$1
#input2=$2

input1="/incoming/2023-04-03_np_PAO26690/"
input2="$input1"


python scripts/concat_fastqgzfiles.py $input1 $input2
#python scripts/tar_fast5.py $input1 $input2
python scripts/move_reports.py $input1 $input2
