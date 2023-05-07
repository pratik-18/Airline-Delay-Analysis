#!/bin/bash

set -e

src_dir=$1
dest_dir="temp"

# Create the destination directory if it doesn't already exist
mkdir -p "$dest_dir"

# Copy all .parquet files from the source directory and its subdirectories to the destination directory with Airline_Delay_Cause_ + the name of the parent directory as the filename
find "$src_dir" -type f -name "*.parquet" -exec sh -c 'cp -v "$0" "$1/Airline_Delay_Cause_$(basename "$(dirname "$0")").parquet"' {} "$dest_dir" \;

#Copy to GCS
gsutil -m cp -r temp/*  gs://ada-cleaned-data-bucket

#Remove temp directory
rm -r temp
