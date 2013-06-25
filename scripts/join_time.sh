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

# Calculate the join time of the nodes

# parameter time hh:mm:ss
to_timestamp(){
  
    s1=`echo $1 | cut -d':' -f 3`
    m1=`echo $1 | cut -d':' -f 2`
    h1=`echo $1 | cut -d':' -f 1`

    ts1=$((10#$h1*3600))+$((10#$m1*60))+$((10#$s1))
    ts1=$(($ts1))
    echo $ts1
}

join_time(){
  
  join_time_groupmanagers
  join_time_localcontrollers

}

join_time_localcontrollers(){
  echo "node start join timestamp_start timestamp_join retry diff" > $tmp_directory/join_localcontrollers.txt 

  for i in `cat $tmp_deploy_directory/local_controllers.txt`
  do
    echo $i
    ts1=`ssh -l root $i cat /tmp/snooze_node.log | head -n 1`
    ts2=`ssh -l root $i cat /tmp/snooze_node.log | grep "Join procedure was successfull"`
    nb=`ssh -l root $i cat /tmp/snooze_node.log | grep "Starting the join procedure" | wc -l`

    h1=`echo $ts1 | cut -d'|' -f2 | cut -d ' ' -f3`
    h2=`echo $ts2 | cut -d'|' -f2 | cut -d ' ' -f3`
    ts1=`to_timestamp $h1`
    ts2=`to_timestamp $h2`
    diff=$((10#$ts2-10#$ts1))
    echo "$i $h1 $h2 $ts1 $ts2 $nb $diff" >> $tmp_directory/join_localcontrollers.txt 
done
}

join_time_groupmanagers(){
  echo "node start join timestamp_start timestamp_join diff" > $tmp_directory/join_groupmanagers.txt 

  for i in `cat $tmp_deploy_directory/group_managers.txt`
  do
    echo $i
    ts1=`ssh -l root $i cat /tmp/snooze_node.log | head -n 1`
    ts2=`ssh -l root $i cat /tmp/snooze_node.log | grep "Starting in .* mode\!"`

    h1=`echo $ts1 | cut -d'|' -f2 | cut -d ' ' -f3`
    h2=`echo $ts2 | cut -d'|' -f2 | cut -d ' ' -f3`
    ts1=`to_timestamp $h1`
    ts2=`to_timestamp $h2`
    diff=$((10#$ts2-10#$ts1))
    echo "$i $h1 $h2 $ts1 $ts2 $diff" >> $tmp_directory/join_groupmanagers.txt 
  done



}

