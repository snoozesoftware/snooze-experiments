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

extract_g5k_machines () {
    local index=0
    for host in `cat $OAR_NODE_FILE | uniq`
    do
        resolved_ip=$(host -t A $host)
        
        if [ $index -eq 0 ];
        then
            echo "${resolved_ip##* }" > $virtual_machine_hosts
            index=$((index+1))
            continue
        fi
        
        echo "${resolved_ip##* }" >> $virtual_machine_hosts
    done
}
