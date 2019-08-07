#!/bin/bash
watch_dir=$(cd $1 && pwd)
tie_basedir=$(cd $(dirname $0)/.. && pwd)
tie="${tie_basedir}/tie.py"
extension_filter="jpg|jpeg|png|bmp|cr2|tiff|gif"

function print_usage(){
    echo "Usage: $(basename $0) images_dir"
    echo "Watches the given directory and updates the tie image index as needed when files are created, moved or deleted"
}

function abort(){
    echo "Error: $@" >&2
    print_usage
    exit -1
}

function handle_file_event(){
    local file_path=$1
    if [[ "${file_path}" =~ \.(${extension_filter})$ ]]; then
        python3 "${tie}" index --frontend batch --files "${file_path}"
    fi
}

function handle_dir_event(){
    local dir_path=$1
    for f in "${dir_path}"/*; do
        handle_event "${f}"  
    done
}

function handle_event(){
    local path=$1
    if [ -f "${path}" ] || [ ! -e "${path}" ]; then
        handle_file_event "${path}"
    elif [ -d "${path}" ]; then
        handle_dir_event "${path}"
    fi
}

function handle_events(){
    while read action file; do
        echo "action:   "${action}
        echo "file:   "${file}
        handle_event "${file}"
    done
}

[ -z "${watch_dir}" ] && abort "Argument missing!"
[ -d "${watch_dir}" ] || abort "Watch dir ${watch_dir} not found!"

shopt -s nocasematch
inotifywait -m -r --format "%e: %w%f" \
    -e MOVED_FROM \
    -e MOVED_TO \
    -e MOVE_SELF \
    -e DELETE \
    -e DELETE_SELF \
    -e CLOSE_WRITE \
     ${watch_dir} | handle_events
