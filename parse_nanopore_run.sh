#!/bin/bash

set -eu

#input1=$1
#input2=$2

input1="test_data/2023-01-24_np_PAM69896/"
input2="out_put/"


python scripts/concat_fastqgzfiles.py $input1 $input2
python scripts/tar_fast5.py $input1 $input2
python scripts/move_reports.py $input1 $input2
