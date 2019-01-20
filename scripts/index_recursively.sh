#!/bin/bash
images_dir=$(cd $1 && pwd)
tie_basedir=$(cd $(dirname $0)/.. && pwd)
tie="${tie_basedir}/tie.py"
extension_filter="jpg\|jpeg\|png\|bmp\|cr2\|tiff\|gif"

function print_usage(){
    echo "Usage: $(basename $0) images_dir"
    echo "Updates the tie index recursively for all files in the given directory"
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

[ -z "${images_dir}" ] && abort "Argument missing!"
[ -d "${images_dir}" ] || abort "Watch dir ${images_dir} not found!"

find "${images_dir}" -type f -iregex ".*\.\(${extension_filter}\)" \
    -exec python3 "${tie}" index --frontend batch --files "{}" \;
