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

# Creates the COW images
create_cow_images () {
    echo "$log_tag Creating COW images for $1"
    for (( I=0; $I < $2; I++ ))
    do
        create_cow_image $1 $I
        if [[ $? -ne $success_code ]]
        then
            return $error_code
        fi
    done  
    
    update_permissions
}

# Creates a single COW image
create_cow_image () {
    echo "$log_tag Creating COW image $2"
    qemu-img create -b $images_location"/"$backing_file_name -f  qcow2 $images_location/$1/$copy_on_write_file_prefix$1-$2".qcow2" 2>&1>/dev/null
    if [[ $? -ne $success_code ]]
    then
        return $error_code
    fi
}
