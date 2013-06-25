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

## Internal script settings
script_name=$(basename $0 .sh)
author="Eugen Feller <eugen.feller@inria.fr>"
log_tag="[Snooze-Experiments]"
snooze_client_binary="/usr/bin/snoozeclient"

## Exit codes
error_code=1
success_code=0

## SSH settings
ssh_private_key="$HOME/.ssh/id_rsa.sid"

## Python location
python="/usr/bin/python"

## SCP tsunami settings 
scp_tsunami_location="/opt/scp-tsunami/scpTsunamiA.py"

## RSYNC settings
export RSYNC_RSH="ssh -i $ssh_private_key"
rsync_location="/usr/bin/rsync"
rsync_parameters="-rtvclgo --progress --delete"

## G5K username
g5k_username="efeller"

############# Snooze deployment settings ##############
local_controllers_file="/home/$g5k_username/snoozedeploy/grid5000/deployscript/tmp/local_controllers.txt"

############# Virtual cluster related settings ########
# User and group
snooze_user="eugen"
snooze_group="eugen"

## Image and template locations
snooze_tmp_directory="/tmp/snooze"
images_location="/home/eugen/Desktop/SVNs/PhD/Software/snoozeclient/trunk/misc/images"
templates_location="/home/eugen/Desktop/SVNs/PhD/Software/snoozeclient/trunk/misc/templates"

## Template name
template_name="debian_kvm.xml"
template_prefix="debian_kvm_"

## Image names
backing_file_distribution="testing"
backing_file_application="web"
backing_file_cluster_location="local"
backing_file_type="raw"
backing_file_name="$backing_file_distribution-$backing_file_application-vm-snooze-$backing_file_cluster_location.$backing_file_type"
copy_on_write_file_prefix="$backing_file_distribution-$backing_file_application-vm-snooze-$backing_file_cluster_location-cow-"

max_memory="297152"
current_memory="297152"
number_of_virtual_cpus="1"

# Networking settings
bridge_name="virbr0"

########### MPI and web benchmark related settings #############
# Temporary directory
tmp_directory="./tmp"

# Total number of iterations
number_of_iterations=3

# Benchmark directory on source and destination
benchmark_directory="/opt"

# Results settings
results_output_directory="./results"

# mpirun settings
mpirun_output_file="$tmp_directory/mpirun_output.log"

# NAS Parallel Benchmark settings
nas_processes_per_node=1
nas_application="ft"
nas_problem_class="A"
nas_working_directory="$benchmark_directory/NPB3.3.1/NPB3.3-MPI/bin"
nas_binary_name="$nas_application.$nas_problem_class.$nas_processes_per_node"
nas_benchmark_binary="$nas_working_directory/$nas_binary_name"
nas_gnuplot_output_file="$results_output_directory/npb/$nas_binary_name.dat"

# Web benchmarks settings
web_cuncurrency=100
web_number_of_requests=1000
web_gnuplot_output_file="$results_output_directory/web/web.dat"

#######################################################

# Client output settings
snoozeclient_output="$tmp_directory/snooze_client_out.txt"
snoozeclient_output_formatted="$tmp_directory/snooze_client_formatted.txt"
virtual_machine_hosts="$tmp_directory/virtual_machine_hosts.txt"

# Submission test case settings
number_of_virtual_clusters=11
virtual_machine_interval=50

# MapReduce test case settings
mapreduce_script="./hadoop/src/suite.py"
mapreduce_filter_compute_and_data_script="./scripts/filter_compute_data_nodes.py"
mapreduce_storage_jobid="430569"
mapreduce_data_nodes_file="./$tmp_directory/data_nodes.txt"
mapreduce_compute_nodes_file="./$tmp_directory/compute_nodes.txt"

# Prints the virtual cluster settings
print_virtual_cluster_settings () {   
    echo "<----------------- Virtual Cluster ------------>"
    echo "$log_tag Images location: $images_location"
    echo "$log_tag Templates location: $templates_location"
    echo "$log_tag Backing file name: $backing_file_name"
    echo "$log_tag Virtual machine max memory: $max_memory"
    echo "$log_tag Virtual machine current memory: $current_memory"
    echo "$log_tag Number of virtual cpus: $number_of_virtual_cpus"
    echo "$log_tag Virtual machine network bridge: $bridge_name"
    echo "<------------------------------------------->"
}

# Prints the general benchmark settings
print_general_benchmark_settings () {   
    echo "<----------------- General benchmark settings ---------------->"
    echo "$log_tag Global benchmark directory: $benchmark_directory"
    echo "$log_tag Global temporary directory: $tmp_directory"
    echo "$log_tag Results output directory: $results_output_directory"
    echo "$log_tag Virtual machine hosts file: $virtual_machine_hosts"
    echo "<------------------------------------------------------------->"
}

# Print NAS parallel benchmark settings
print_npb_settings () {   
    echo "<----------------- Nas parallel benchmark settings ------------>"
    echo "$log_tag MPIRUN output file: $mpirun_output_file"
    echo "$log_tag GNUPlot output file: $gnuplot_output_file_npb"
    echo "$log_tag Number of processes per node: $nas_processes_per_node"
    echo "$log_tag Application: $nas_application"
    echo "$log_tag Problem class: $nas_problem_class"
    echo "$log_tag Nodes working directory: $nas_working_directory"
    echo "$log_tag Benchmark directory: $nas_benchmark_directory"
    echo "$log_tag Benchmark binary: $nas_benchmark_binary"
    echo "<-------------------------------------------------------------->"
}

# Prints the web settings
print_web_settings () {
    echo "<------------------- Web benchmark settings -------------------->"
    echo "$log_tag Cuncurrentcy: $web_cuncurrency"
    echo "$log_tag Number of requests: $web_number_of_requests" 
    echo "$log_tag Output file: $web_gnuplot_output_file"
    echo "<-------------------------------------------------------------->"
}
