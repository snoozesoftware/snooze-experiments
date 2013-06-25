#!/bin/bash
#
# Copyright (C) 2010-2012 Eugen Feller, INRIA <eugen.feller@inria.fr>
#
# This file is part of Snooze, a scalable, autonomic, and
# energy-aware virtual machine (VM) management framework.
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses>.
#

source $scriptpath/scripts/common.sh
source $scriptpath/scripts/transfer.sh
source $scriptpath/scripts/mpirun.sh

# Generates  gnuplot file from NPB output
generate_gnuplot_output () {
    echo "$log_tag Generating GNUPlot file"
    echo "$1 $2" >> $nas_gnuplot_output_file
}

# Returns the time in seconds
get_npb_time_in_seconds () {
    local time_in_seconds=$(cat $mpirun_output_file | grep "Time in seconds" | awk '{ print $5 }')
    echo $time_in_seconds
}

# Returns the total number of processes
get_npb_total_processes () {
    local total_processes=$(cat $mpirun_output_file | grep "Total processes" | awk '{ print $4 }')
    echo $total_processes
}

# Synchronizes nas parallel benchmark on all virtual machines
synchronize_benchmark () {
    echo "$log_tag Synchronizing NAS parallel benchmark on all virtual machines"
    for virtual_machine in $(cat "$virtual_machine_hosts"); do
        synchronize_with_rsync $virtual_machine $benchmark_directory "/"
    done 
}

# Starts the actual benchmark
run_benchmark () {
    local total_execution_time=0.0
    local number_of_virtual_machines=$(get_number_of_virtual_machines)
    echo "$log_tag Running the NAS parallel benchmark $number_of_iterations times on $number_of_virtual_machines virtual machines"
    for (( I=0; $I < $number_of_iterations; I++ ))
    do
        start_mpirun $number_of_virtual_machines $virtual_machine_hosts $nas_working_directory $nas_benchmark_binary
        local current_execution_time=$(get_npb_time_in_seconds)
        echo "$log_tag Execution time during round $I was $current_execution_time"
        total_execution_time=`echo $total_execution_time + $current_execution_time | bc`
    done 
    
    local average_execution_time=$(echo – | awk "{print $total_execution_time/$number_of_iterations}")
    echo "$log_tag Average execution time was $average_execution_time"
    generate_gnuplot_output $number_of_virtual_machines $average_execution_time
}

# Starts the nas parallel benchmark
start_nas_parallel_benchmark () {
    echo "$log_tag Starting NAS parallel benchmark: $1"
    case "$1" in
    'sync') echo "$log_tag Synchronizing the benchmark"
        synchronize_benchmark
        ;;
    'run') echo "$log_tag Running the benchmark"
        run_benchmark
        ;;
    *) echo "$log_tag Unknown command received!"
       ;;
    esac
}
