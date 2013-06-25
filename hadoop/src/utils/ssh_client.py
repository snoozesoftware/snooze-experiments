#
# Copyright (C) 2010-2012 Eugen Feller, INRIA <eugen.feller@inria.fr>
# based on the work from Ancuta Iordache, INRIA <ancuta.iordache@inria.fr>
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

import paramiko
import logging

from config import settings
from multiprocessing import Pool

logger = logging.getLogger(__name__) 

class SSHClient:
    '''
    Runs shell commands over SSH
    '''

    def __init__(self):
        pass
        
    def __run_commands(self, host, commands, connection):
        '''
        Executes a list of commands on a host
        '''
        
        for command in commands:
            logger.debug("host: %s, command: %s" % (host, command))
            
            try:
                session = connection.get_transport().open_session()
                session.set_combine_stderr(True)
                session.exec_command(command)
            except Exception, e:
                logger.error("Command execution failed: %s" % str(e))
            
            output = ''
            try:
                part = session.recv(65536)
                while part:
                    output += part
                    part = session.recv(65536)
            except Exception, e:
                logger.error("Error reading output: %s" % str(e))
                return
                
            logger.debug("host %s output: %s" % (host, output))
            
            status = session.recv_exit_status()
            if status > 0:
                logger.error("host: %s failed : Command execution status: %s" % (host, status))
                
    def __call__(self, args):
        '''
        Run command wrapper
        '''
        
        return self.run_commands_on_host(*args)


    def run_distinct_commands_on_hosts(self, hosts_dict, username, password):
        '''
        Runs the commands in parallel on the remote hosts
        '''
        
        pool = Pool(len(hosts_dict))
        parameters = [(host, commands, username, password) for host, commands in hosts_dict.iteritems()]
        pool.map(self, parameters)
        pool.close()
        pool.join()
        
    def run_same_commands_on_hosts(self, hosts, commands, username, password):
        '''
        Runs the commands in parallel on the remote hosts
        '''
        
        pool = Pool(len(hosts))
        parameters = [(host, commands, username, password) for host in hosts]
        pool.map(self, parameters)
        pool.close()
        pool.join()
        
    def run_commands_on_host(self, host, commands, username, password):
        '''
        Runns commands on a remote host
        '''
        
        connection = self.__createConnection(host, username, password)
        self.__run_commands(host, commands, connection)
        connection.close()

    def __createConnection(self, host, username, password):
        '''
        Estabilishes an SSH connection with the host
        '''
        
        retry_count = settings.SYSTEM_SSH_RETRY_COUNT
        is_error = True
        connection  = None

        while is_error and retry_count > 0:
            try:
                connection = paramiko.SSHClient()
                connection.load_system_host_keys()
                connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                connection.connect(host, username=username, password=password)
                is_error = False
            except Exception, e:
                del connection
                connection = None
                retry_count = retry_count - 1
                logger.error("Failed connecting to %s, Reason: %s, Retrying %s times more." % (host, 
                                                                                               str(e), 
                                                                                               retry_count))
                
        if connection is None:
            raise Exception("Failed connecting to: %s" % host)
        else:
            logger.debug("Connection to host %s successfull" % host)

        return connection
