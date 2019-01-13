#!/bin/bash
set -e
function print_usage(){
    cat << EOF
Usage: $(basename $0) all|any
EOF
}
function abort(){
    echo "Error: $@" >&2
    exit -1
}
if [ "x$1" == "x-h" ] || [ "x$1" == "x--help" ];then
    print_usage
    exit 0
fi
basedir=$(dirname $0)/..
matchtype=$1
case $matchtype in
    'all'|'any')
        result=$(${basedir}/tie.py query -F gtk -m $matchtype)
        ;;
    *)
        abort "Invalid matchtype $matchtype"
        ;;
esac

[ -z "$result" ] && abort "No results found"
export IFS=$'\n'
${VIEWER:-gthumb} $result
