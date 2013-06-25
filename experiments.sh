#!/bin/bash
#
# Copyright (C) 2011-2012 Eugen Feller, INRIA <eugen.feller@inria.fr>
#
# This file is part of Snooze. Snooze is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA
#

scriptpath=$(dirname $0)
source $scriptpath/scripts/settings.sh
source $scriptpath/scripts/cow_images.sh
source $scriptpath/scripts/templates.sh
source $scriptpath/scripts/cluster.sh
source $scriptpath/scripts/grid5000.sh
source $scriptpath/scripts/image_propagation.sh
source $scriptpath/scripts/taktuk.sh
source $scriptpath/scripts/nas_parallel_benchmark.sh
source $scriptpath/scripts/web.sh
source $scriptpath/scripts/permissions.sh
source $scriptpath/scripts/submission_test_case.sh
source $scriptpath/scripts/mapreduce_benchmark.sh

# Prints the usage information
print_usage () {
    echo "Usage: $script_name [options]"
    echo "Contact: $author"
    echo "Options:"
    echo "-p                                             Extract G5K machines list"
    echo "-b                                             Propagate VM base image"
    echo "-c  [name]  [nVMs]                             Create virtual cluster"
    echo "-i  [name]                                     Propagate virtual cluster"
    echo "-s  [name]                                     Start virtual cluster"
    echo "-d  [name]                                     Destroy virtual cluster"
    echo "-r  [name]                                     Remove virtual cluster"
    echo "-t  [create/start/remove]                      Submission test case"
    echo "-m  [start/auto/storage/configure/benchmark]   Start MapReduce benchmark"
    echo "-n  [sync/run]                                 Start NPB (NAS Parallel Benchmark)"
    echo "-w  [hostname]                                 Start web benchmark (Pressflow)"
}

# Process the user input
option_found=0
while getopts ":c:bi:s:d:r:t:pm:n:w:" opt; do
    option_found=1
    case $opt in
        c)
            print_virtual_cluster_settings
            name=$OPTARG
            eval "number_of_virtual_machines=\${$OPTIND}"
            shift 2
            prepare_and_create_virtual_cluster $name $number_of_virtual_machines
            return_value=$?
            ;;
        b)
            propagate_base_image
            return_value=$?
            ;;
        i)
            propagate_virtual_cluster $OPTARG
            return_value=$?
            ;;
        s)
            start_virtual_cluster $OPTARG
            return_value=$?
            ;;
        d)
            destroy_virtual_cluster $OPTARG
            return_value=$?
            ;;
        r)
            remove_virtual_cluster $OPTARG
            return_value=$?
            ;;
        t)
            start_submission_test_case $OPTARG
            return_value=$?
            ;;
        p)
            extract_g5k_machines
            return_value=$?
            ;;
        m)
            start_mapreduce_benchmark $OPTARG
            return_value=$?
            ;;
        n)
            print_npb_settings
            start_nas_parallel_benchmark $OPTARG
            return_value=$?
            ;;
        w)
            print_web_settings
            start_web_benchmark $OPTARG
            return_value=$?
            ;;
        \?)
            echo "$log_tag Invalid option: -$OPTARG" >&2
            print_usage
            exit $error_code
            ;;
        :)
            echo "$log_tag Missing argument for option: -$OPTARG" >&2
            print_usage
            exit $error_code
            ;;
    esac
done

if ((!option_found)); then
    print_usage 
    exit $error_code
fi

if [[ $? -ne $return_value ]]
then
    echo "$log_tag Command failed!" >&2
    exit $error_code
fi

echo "$log_tag Command executed successfully!" >&2
exit $success_code
