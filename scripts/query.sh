#!/bin/bash
set -e
function print_usage(){
    cat << EOF
Usage: $(basename $0) all | any | anyof n

where
    all:
        uses match type "all"
    any:
        uses match type "any"
    anyof:
        uses match type "all" for the provided arguments but reads arguments "n" times and joins all results
EOF
}
function abort(){
    echo "Error: $@" >&2
    exit -1
}
function run_n_times(){
    n=${1}
    [[ -z ${n} ]] && abort "Argument \"n\" missing!"
    [[ "${n}" =~ [0-9]+ ]] || abort "Argument \"n\" must be an integer value!"
    result=""
    while [ ${n} -gt 0 ]; do
       ${basedir}/tie.py query -F gtk -m all
       ((n--))
    done
}
if [ "x$1" == "x-h" ] || [ "x$1" == "x--help" ];then
    print_usage
    exit 0
fi

basedir="$(dirname $0)/.."
matchtype="${1}"
case ${matchtype} in
    'all'|'any')
        result=$(${basedir}/tie.py query -F gtk -m ${matchtype})
        ;;
    'anyof')
        n="${2}"
        [[ -z ${n} ]] && abort "Argument \"n\" missing!"
        [[ "${n}" =~ [0-9]+ ]] || abort "Argument \"n\" must be an integer value!"
        result=$(run_n_times ${n} | sort -u)
        ;;
    *)
        abort "Invalid matchtype $matchtype"
        ;;
esac

#exit


[ -z "${result}" ] && abort "No results found"
export IFS=$'\n'
${VIEWER:-gthumb} ${result}
