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

perform_virtual_cluser_tasks () 
{
    echo "$log_tag Creating virtual cluster, propagating images, and starting"
    prepare_and_create_virtual_cluster $1 $2
    propagate_base_image
    propagate_virtual_cluster $1
    start_virtual_cluster $1
}

variable_data () {
    local master_node=$(get_hadoop_master_node)
    local data_nodes=`cat $virtual_machine_hosts | sed -n 2,"$(($1+1))"p`
    local compute_nodes=`cat $virtual_machine_hosts | sed -n $(($1+2)),"$(($2+$2+1))"p`
    echo "$log_tag Configuring MapReduce in variable mode on master node: $master_node, data nodes: $data_nodes and compute nodes: $compute_nodes"
    $python "$mapreduce_script" "mapreduce_separatedata" "--master" $master_node "--data" $data_nodes "--compute" $compute_nodes
}

normal () {
    local master_node=$(get_hadoop_master_node)
    local slave_nodes=$(get_virtual_machine_hosts_not_first)
    echo "$log_tag Configuring MapReduce in normal mode on master: $master_node and slaves: $slave_nodes"
    $python "$mapreduce_script" "mapreduce_normal" "--master" $master_node "--slaves" $slave_nodes
}

configure_mapreduce ()
{
    case "$1" in
    'normal')
        echo "$log_tag Configuring MapReduce with variable number of compute and data VMs"
        normal
        ;;
    'variable_data') 
        echo "$log_tag Configuring MapReduce with co-located data and compute"
        echo "$log_tag Number of data nodes:"
        read number_of_data_nodes
        echo "$log_tag Number of compute nodes:"
        read number_of_compute_nodes
        variable_data $number_of_data_nodes $number_of_compute_nodes
        ;;
    *) echo "$log_tag Unknown command received!"
       ;;
    esac
}

execute_ssh_command() {
    echo "$log_tag Sending $2 command over SSH to $1"
    $ssh_command $HADOOP_USER@$1 "$2"
}

run_terasort() {
    for size in $TERAGEN_INPUT_SIZES
    do
        teragen_dat="teragen_$size.dat"
        execute_ssh_command $1 "$TERASORT_RMDIR_INPUT"
        execute_ssh_command $1 "$TERAGEN_HADOOP_BIN $size $TERASORT_INPUT_DIR 2>> $HADOOP_RESULTS/$2_$teragen_dat"
        execute_ssh_command $1 "sleep $SYSTEM_SLEEP_TIME"
        terasort_dat="terasort_$size.dat"
        execute_ssh_command $1 "$TERASORT_RMDIR_OUTPUT"
        execute_ssh_command $1 "$TERASORT_HADOOP_BIN 2>> $HADOOP_RESULTS/$2_$terasort_dat" 
        execute_ssh_command $1 "sleep $SYSTEM_SLEEP_TIME"
    done

    execute_ssh_command $1 "$TERASORT_RMDIR_INPUT"
    execute_ssh_command $1 "$TERASORT_RMDIR_OUTPUT"
}

run_wikipedia() {
    execute_ssh_command $1 "$WIKIBENCH_RMDIR_INPUT"
    execute_ssh_command $1 "$WIKIBENCH_MKDIR_INPUT"

    for run in $WIKIBENCH_RUNS
    do
        source_file_name=$WIKIBENCH_INPUT_DATA_DIR/$WIKIBENCH_INPUT_FILE
        destination_file_name=$WIKIBENCH_INPUT_DIR/$WIKIBENCH_INPUT_FILE$run
        echo "Uploading $source_file_name in round $run to $destination_file_name"
        execute_ssh_command $1 "$HADOOP_COPY_FROM_LOCAL $source_file_name $destination_file_name 2>> $HADOOP_RESULTS/$2_wikidata_$run.dat"
        execute_ssh_command $1 "sleep $SYSTEM_SLEEP_TIME"
        for mode in $WIKIBENCH_MODES 
        do
            echo "$log_tag Running Wikipedia benchmark in mode $mode"
            execute_ssh_command $1 "$WIKIBENCH_HADOOP_BIN $mode $HADOOP_MAPS $HADOOP_REDUCES $WIKIBENCH_INPUT_DIR $WIKIBENCH_OUTPUT_DIR 2>> $HADOOP_RESULTS/$2_wikibench_"$run"_"$mode".dat"
            execute_ssh_command $1 "$WIKIBENCH_RMDIR_OUTPUT"
            execute_ssh_command $1 "sleep $SYSTEM_SLEEP_TIME"
      done
    done

    execute_ssh_command $1 "$WIKIBENCH_RMDIR_INPUT"
    execute_ssh_command $1 "$WIKIBENCH_RMDIR_OUTPUT"
}

auto_case_proportions ()
{
    echo "$log_tag Enter the node numbes (e.g. 10 45 90)"
    while read line
    do
        nodes=("${nodes[@]}" $line)
    done

    size=${#nodes[@]}
    for number_of_data_nodes in "${nodes[@]}"
    do
        echo "$log_tag Taking $number_of_data_nodes as data"
        for number_of_compute_nodes in ${nodes[@]:0:$size}
        do
            echo "$log_tag Taking $number_of_compute_nodes as compute"
            variable_data $number_of_data_nodes $number_of_compute_nodes
            run_benchmarks "$number_of_data_nodes-$number_of_compute_nodes"
        done
        size=$((size - 1))
    done
}

run_benchmarks ()
{
    local master_node=$(get_hadoop_master_node)
    run_terasort $master_node $1
    run_wikipedia $master_node $1
}

automated_run () {
    echo "$log_tag Starting fully automated MapReduce run! Select the case (prop, bench):"
    read case
    case "$case" in
    'prop')
        echo "$log_tag Starting running the proportions case"
        auto_case_proportions
        ;;
    'bench') 
        echo "$log_tag Started running the benchmarks case"
        run_benchmarks "manual"
        ;;
    *) echo "$log_tag Unknown command received!"
       ;;
    esac
}

start_mapreduce_benchmark () 
{
    case "$1" in
    'start')
        echo "$log_tag Cluster name:"
        read cluster_name
        echo "$log_tag Number of VMs:"
        read number_of_vms
        perform_virtual_cluser_tasks $cluster_name $number_of_vms
        ;;
    'auto')
        automated_run
        ;;
    'storage')
        local hosts_list=$(get_virtual_machine_hosts)
        $python $mapreduce_script "storage" "--hosts" $hosts_list "--job_id" $mapreduce_storage_jobid
        ;;
    'configure') 
        echo "$log_tag Configuration mode (normal, variable_data):"
        read configuration_mode
        configure_mapreduce $configuration_mode
        ;;
    'benchmark')
        echo "$log_tag Benchmark name (e.g. dfsio, dfsthroughput, mrbench, nnbench, \
               pi, teragen, terasort, teravalidate, censusdata, censusbench, wikidata, wikibench):"
        read benchmark_name
        local master_node=$(get_hadoop_master_node)
        $python "$mapreduce_script" "benchmark" "--name" $benchmark_name "--master" $master_node
        ;;
    *) echo "$log_tag Unknown command received!"
       ;;
    esac
}
