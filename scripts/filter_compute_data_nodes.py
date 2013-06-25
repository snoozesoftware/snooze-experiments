#!/usr/bin/env python
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

import sys

def write_output(file_name, output):
    file = open(file_name, "w")
    file.write(" ".join(output))

def convert_output(file_name):
    fd = open(file_name)
    map = {}
    lines = fd.readlines()
    for content in lines:
         splitted = content.split()
         host = splitted[1]
         if host in map:
            vms = map[host]
            vms.append(splitted[0])
         else:
            vms = [splitted[0]]
            map.update({splitted[1]:vms})

    data_nodes, compute_nodes = [], []
    for host in map:
        data_nodes.append(map[host][0])
        compute_nodes.extend(map[host][1:])
        
    return data_nodes, compute_nodes
    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.stderr.write('Usage: ./filter_compute_data_nodes.py snooze_output_file data_node_file compute_node_file\n')
        sys.exit(1)
    
    data_nodes, compute_nodes = convert_output(sys.argv[1])
    write_output(sys.argv[2], data_nodes)
    write_output(sys.argv[3], compute_nodes)
