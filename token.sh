#! /bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 input-directory output-directory"
    exit 1
fi

input_directory=$1
output_directory=$2

mkdir -p "$output_directory"

for input_file in "$input_directory"/*.txt; do
    if [ -f "$input_file" ]; then
        # Create output file name by replacing the input file with the output file
        output_file="$output_directory/$(basename "${input_file}.txt")"
        # Run token.py on each file 
        python token.py "$input_file" "$output_file"
        # Was file actually created?
        if [ -f "$output_file" ]; then
            echo "Processed $input_file -> $output_file"
        else
            echo "Error: Output file $output_file not created."
        fi
else
    echo "Error: Input file $input_file not found."
fi
done