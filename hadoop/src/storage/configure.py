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

import os
import pwd

from config import settings
from utils.ssh_client import SSHClient
from multiprocessing import Pool

class StorageConfiguration(object):
    '''
    Storage configuration
    '''

    def __init__(self, job_id, all_hosts):
        '''
        Constructor
        '''
        self.__job_id = job_id
        self.__all_hosts = all_hosts
        self.__sshClient = SSHClient()
        
    # Broken for VMs!
    def configure_and_mount_nfs(self):
        '''
        Configuring all_hosts
        '''

        # To access G5K mount point from VMs
        uid_set_command = "usermod -u" + settings.WHITESPACE + settings.G5K_USERID + settings.WHITESPACE \
                          + settings.SYSTEM_HADOOP_USER_NAME
                    
        # To mount NFS directory
        mount_command = "mount -t nfs" + settings.WHITESPACE + settings.NFS_STORAGE_SERVER + ":/data/" \
                        + settings.G5K_USERNAME + "_" + self.__job_id + settings.WHITESPACE + settings.NFS_MOUNT_DIRECTORY
                        
        # Chown hadoop directory
        commands = [settings.HADOOP_CHOWN, uid_set_command, settings.SYSTEM_UMOUNT_NFS, mount_command]
        
        self.__sshClient.run_same_commands_on_hosts(self.__all_hosts, 
                                                    commands, 
                                                    settings.SYSTEM_ROOT_USER_NAME, 
                                                    settings.SYSTEM_ROOT_USER_PASSWORD)
