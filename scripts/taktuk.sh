#!/bin/bash
#
# Copyright (C) 2011-2012 Eugen Feller, INRIA <eugen.feller@inria.fr>
#
# This file is part of Snooze. Snooze is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA
#

# Runs the taktuk command on a list of machines
run_taktuk () {
    echo "taktuk -c $ssh_command_taktuk -l root -s -f $1 broadcast $2 $3"
    taktuk -c "$ssh_command_taktuk" -l root -s -f $1 broadcast $2 $3 
}

# Runs the taktuk command on a single machine
run_taktuk_single_machine () {
    taktuk -c "$ssh_command_taktuk" -l root -s -m $1 broadcast $2 $3
}

#put files on list host $1 
put_taktuk () {
    echo "taktuk -c $ssh_command_taktuk -l root -s -f $1 broadcast put { $2 } { $3 }"
    taktuk -c "$ssh_command_taktuk" -l root -s -f $1 broadcast put { $2 } { $3 } 
}
