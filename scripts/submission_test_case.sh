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

create_virtual_clusters ()
{
    local number_of_virtual_machines=0
    for (( i=1; i <= $number_of_virtual_clusters; i++ ))
    do 
        cluster_name="mycluster$i"
        if [ $i -eq 1 ];
        then
            prepare_and_create_virtual_cluster $cluster_name $i
        else
            number_of_virtual_machines=$(($number_of_virtual_machines+$virtual_machine_interval))
            prepare_and_create_virtual_cluster $cluster_name $number_of_virtual_machines
        fi
    done
}

start_virtual_clusters () {
    for (( i=1; i <= $number_of_virtual_clusters; i++ ))
    do 
        cluster_name="mycluster$i"
        if [ $i -eq 1 ];
        then
            start_virtual_cluster $cluster_name
            destroy_virtual_cluster $cluster_name
        else
            start_virtual_cluster $cluster_name
            destroy_virtual_cluster $cluster_name
        fi
    done
}

remove_virtual_clusters () {
    for (( i=1; i <= $number_of_virtual_clusters; i++ ))
    do 
        cluster_name="mycluster$i"
        if [ $i -eq 1 ];
        then
            remove_virtual_cluster $cluster_name
        else
            remove_virtual_cluster $cluster_name
        fi
        
        sleep 5
    done
}

start_submission_test_case () {
    echo "$log_tag Submission test case action: $1"
    case "$1" in
    'create') echo "$log_tag Creating virtual clusters"
        create_virtual_clusters
        ;;
    'start') echo "$log_tag Starting vitual clusters"
        start_virtual_clusters
        ;;
    'remove') echo "$log_tag Removing virtual clusters"
        remove_virtual_clusters
        ;;
    *) echo "$log_tag Unknown command received!"
       ;;
    esac
}
