#!/bin/bash

PATH=/usr/bin:/usr/sbin

input_file=${1:-"to_transform.text"}
output_file=${2:-"out.data"}
ckpt=${3:-"checkpoints/checkpoint_average_best-3.pt"}
medium_file="${input_file%.*}.bpe.${input_file##*.}"

python scripts/multiprocessing_bpe_encoder.py \
    --encoder-json encoder.json \
    --vocab-bpe vocab.bpe \
    --inputs "${input_file}" \
    --outputs "${medium_file}" \
    --workers 60 \
    --keep-empty

fairseq-interactive data/rotowire/bins \
    --path $ckpt --beam 5 --remove-bpe --buffer-size 1024 \
    --max-tokens 8192 --max-len-b 1024 \
    --user-dir src/ --task text_to_table_task --table-max-columns 38 \
    > ${output_file} < ${medium_file}

bash scripts/eval/convert_fairseq_output_to_text.sh ${output_file}
