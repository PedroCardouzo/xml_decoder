#!/bin/bash

PROGRAM_NAME="xml_decoder.py"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

PROGRAM="$DIR"/"$PROGRAM_NAME"

if [ -f "$1" ]; then  # if provided a file, use the file data
	INPUT_FILE="$1"
	in_data="$(cat "$1")"
else				  # if not, use stdin
	INPUT_FILE="stdin"
	in_data="$(cat)"
fi

# remove <root> and </root> tags


# remove <root> and </root> tags
in_data=${in_data##<[Rr]oot>>};
in_data=${in_data%%<\/[Rr]oot>};

output="$(echo "$in_data" | python3 $PROGRAM)"

if [ $INPUT_FILE != "stdin" ]; then  # if provided a file, output to a file with same name, but _view appended to the end
	echo "$in_data" > "$INPUT_FILE"; # overwrite input file with valid data
	out_filename=$(echo $1 | cut -d'.' -f1)
	file_termination=$(echo $1 | cut -d'.' -f2)
	echo "$output" > "$out_filename""_view.""$file_termination"
else				  # else, just send the output to stdout
	echo "$output"
fi

