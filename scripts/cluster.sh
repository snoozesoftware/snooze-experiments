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

# Adds virtual cluster directories
create_virtual_custer_directories () {
    echo "$log_tag Creating virtual cluster directories for $1"
    mkdir -p "$images_location/$1" > /dev/null 2>&1
    mkdir -p "$templates_location/$1" > /dev/null 2>&1
}

# Removes the virtual cluster directories
remove_virtual_cluster_directories () {
    echo "$log_tag Removing images and templates for virtual cluster: $1"
    rm -Rf "$images_location/$1"
    rm -Rf "$templates_location/$1"
}

# Starts the virtual cluster creation
prepare_and_create_virtual_cluster () {
    echo "$log_tag Starting virtual cluster creation!"
    create_virtual_custer_directories $1
    if [[ $? -ne $success_code ]]
    then
        return $error_code
    fi
    
    create_cow_images $1 $2
    if [[ $? -ne $success_code ]]
    then
        return $error_code
    fi
    
    create_virtual_machine_templates $1 $2
    if [[ $? -ne $success_code ]]
    then
        return $error_code
    fi
    
    create_virtual_cluster $1 $2
    if [[ $? -ne $success_code ]]
    then
        return $error_code
    fi
}

# Creates the virtual cluster
create_virtual_cluster () {
    echo "$log_tag Creating virtual cluster $1"
    $snooze_client_command define -vcn $1
    if [[ $? -ne $success_code ]]
    then
        return $error_code
    fi
    
    for (( I=0; $I < $2; I++ ))
    do
        $snooze_client_command add -vcn $1 -vmt "$templates_location/$1/$template_prefix$1_$I.xml" 
    done 
}

# Starts the virtual cluster
start_virtual_cluster ()
{
    echo "$log_tag Starting virtual cluster: $1"
    echo "$snooze_client_command start -vcn $1 > $snoozeclient_output"
    $snooze_client_command start -vcn $1 > $snoozeclient_output
    format_snooze_output
    generate_virtual_machine_hosts_list
}

# Destroy the virtual cluster
destroy_virtual_cluster ()
{
    echo "$log_tag Destroy virtual cluster: $1"
    $snooze_client_command destroy -vcn $1
}

# Removes the virtual cluster
remove_virtual_cluster () {
    echo "$log_tag Removing virtual cluster $1"
    $snooze_client_command undefine -vcn $1
    if [[ $? -ne $success_code ]]
    then
        return $error_code
    fi
    
    remove_virtual_cluster_directories $1
}
