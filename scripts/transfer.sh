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

fix_permissions () {
    echo "$log_tag Fixing permissions of directory $2 on remote host $1"
    $ssh_command $1 "chown -R $snooze_user:$snooze_group $2"
}

# Synchronized data using rsync
synchronize_with_rsync () {
    echo "$log_tag Synchronizing data $2 to directory $3 on node $1 RSYNC"
    $rsync_command $2 $host_root_username@$1:$3 > /dev/null 2>&1
}

# Synchronized data using scp
synchronize_with_scp () {
    echo "$log_tag Synchronizing data $2 to directory $3 on node $1 with SCP"
    $scp_command $2 $host_root_username@$1:$3 > /dev/null 2>&1
    fix_permissions $1 $3
}

synchronize_with_tsunami (){
    echo "$log_tag Synchronizing data $1 to directory $2 with TSUNAMI"
    # zip the directory
    tar -zcf /tmp/bases.tar.gz $1
    $scp_tsunami_command /tmp/bases.tar.gz /bases.tar.gz -u root -f $local_controllers_file
}
