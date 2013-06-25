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

# Creates virtual machine templates
create_virtual_machine_templates () {
    echo "$log_tag Creating virtual machine templates for $1"
    for (( I=0; $I < $2; I++ ))
    do
        create_virtual_machine_template $1 $I
        if [[ $? -ne $success_code ]]
        then
            return $error_code
        fi
    done  
    
    update_permissions
}

# Creates a single virtual machine template
create_virtual_machine_template () {
    echo "$log_tag Creating virtual machine template $2"
    
    # Set name
    sed 's#<name>.*#<name>'$template_prefix$1_$2'</name>#' "./templates/$template_name" > "$templates_location/$1/$template_prefix$1_$2.xml" 
    if [[ $? -ne $success_code ]]
    then
        return $error_code
    fi
    
    # Set random uuid
    random_uuid=$(python  -c 'import uuid; print uuid.uuid1()')
    perl -pi -e "s#<uuid>.*#<uuid>$random_uuid</uuid>#" "$templates_location/$1/$template_prefix$1_$2.xml" 
    # Set max memory
    perl -pi -e "s#<memory>.*#<memory>$max_memory</memory>#" "$templates_location/$1/$template_prefix$1_$2.xml" 
    # Set current memory
    perl -pi -e "s#<currentMemory>.*#<currentMemory>$current_memory</currentMemory>#" "$templates_location/$1/$template_prefix$1_$2.xml" 
    # Set number of virtual cpus
    perl -pi -e "s#<vcpu>.*#<vcpu>$number_of_virtual_cpus</vcpu>#" "$templates_location/$1/$template_prefix$1_$2.xml" 
    # Set image location
    # perl -pi -e "s#<source file.*#<source file='$images_location/$1/$copy_on_write_file_prefix$1-$2.qcow2'/>#" "$templates_location/$1/$template_prefix$1_$2.xml" 

    # Disk image
    perl -pi -e "s#<<diskimage>>#$images_location/$1/$copy_on_write_file_prefix$1-$2.qcow2#" "$templates_location/$1/$template_prefix$1_$2.xml"
    # Cdrom image
    perl -pi -e "s#<<cdromimage>>#$images_location/$context_image#" "$templates_location/$1/$template_prefix$1_$2.xml"


    # Set bridge name
    perl -pi -e "s#<source bridge.*#<source bridge='$bridge_name'/>#" "$templates_location/$1/$template_prefix$1_$2.xml" 
}
