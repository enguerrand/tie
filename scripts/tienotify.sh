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

function handle_events(){
    while read action file; do
        if [[ "${file}" =~ \.(${extension_filter})$ ]]; then
            echo "action:   "${action}
            echo "file:   "${file}
            python3 "${tie}" index --frontend batch --files "${file}"
        fi
    done
}

[ -z "${watch_dir}" ] && abort "Argument missing!"
[ -d "${watch_dir}" ] || abort "Watch dir ${watch_dir} not found!"

shopt -s nocasematch
inotifywait -m -r --format "%e: %w%f" \
    -e MOVED_FROM \
    -e MOVED_TO \
    -e DELETE \
    -e MODIFY \
    -e CLOSE_WRITE \
     ${watch_dir} | handle_events
