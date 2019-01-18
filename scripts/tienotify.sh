#!/bin/bash
watch_dir=$1
tie_basedir=$(cd $(dirname $0)/.. && pwd)
tie="${tie_basedir}/tie.py"

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
        echo "action:   "$action
        echo "file:   "$file
        python3 "${tie}" index --frontend batch --files "$file"
    done
}

[ -z "${watch_dir}" ] && abort "Argument missing!"
[ -d "${watch_dir}" ] || abort "Watch dir ${watch_dir} not found!"

inotifywait -m -r --format "%e: %w%f" \
    -e MOVED_FROM \
    -e MOVED_TO \
    -e DELETE \
    -e MODIFY \
    -e CLOSE_WRITE \
     ${watch_dir} | handle_events
