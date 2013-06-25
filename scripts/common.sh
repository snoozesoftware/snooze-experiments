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

get_number_of_virtual_machines () {
    local number_of_vms=`cat $virtual_machine_hosts | wc -l`
    echo $number_of_vms
}

get_virtual_machine_hosts_not_first() {
    local hosts=`cat $virtual_machine_hosts | tail -n +2 | sed -n -e ":a" -e "$ s/\n/ /gp;N;b a"`
    echo $hosts
}

get_virtual_machine_hosts () {
    local hosts=`cat $virtual_machine_hosts | sed -n -e ":a" -e "$ s/\n/ /gp;N;b a"`
    echo $hosts
}

get_hadoop_master_node () {
    local first_host=`cat $virtual_machine_hosts | head -n 1`
    echo $first_host
}

format_snooze_output() {
    cat $snoozeclient_output | awk '{ print $2, $4 }' | egrep "[0-9]{1,}" > $snoozeclient_output_formatted
}

generate_virtual_machine_hosts_list ()  {
    cat $snoozeclient_output | awk '{print $2}' | egrep "[0-9]{1,}" > $virtual_machine_hosts
}    
