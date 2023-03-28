#!/bin/bash

set -eu

#input1=$1
#input2=$2

input1="/incoming/2022-12-13_np_PAM70460/"
input2="/incoming/2022-12-13_np_PAM70460/"


python scripts/concat_fastqgzfiles.py $input1 $input2
python scripts/tar_fast5.py $input1 $input2
python scripts/move_reports.py $input1 $input2
