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

import time
import logging

from pprint import pprint
from config import settings
from utils.ssh_client import SSHClient
from utils.string_utils import remove_dots
from multiprocessing import Pool

logger = logging.getLogger(__name__)

class HadoopConfigureNormal(object):
    '''
    Hadoop related logic.
    '''
    
    def __init__(self, master_host, slave_hosts, storage_mode):
        self.master_host = master_host
        self.slave_hosts = slave_hosts
        self.__storage_mode = storage_mode
        self.__hosts = [master_host] + slave_hosts
        self.sshClient = SSHClient()
        
    def __configure_master_host(self):
        # Clear master_host/slave files and add master_host host address to the hadoop master_hosts file
        commands = [settings.HADOOP_CLEAN_SLAVES_FILE,
                    "echo " + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(self.master_host) + " > " \
                    + settings.HADOOP_MASTER_FILE]
        
        # add slave hosts ip to hadoop slave_hosts file
        for host in self.slave_hosts:        
            commands.append("echo " + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(host) + " >> " + \
                             settings.HADOOP_SLAVES_FILE)
                    
        if self.__storage_mode == "nfs":
            commands.append(settings.HADOOP_START_MAPRED)
        elif self.__storage_mode == "hdfs":
            commands.append(settings.HADOOP_FORMAT_DFS)
            commands.append(settings.HADOOP_START_ALL_SERVICES)    
            
        # run the commands on the master_host host
        self.sshClient.run_commands_on_host(self.master_host, 
                                            commands, 
                                            settings.SYSTEM_HADOOP_USER_NAME, 
                                            settings.SYSTEM_HADOOP_USER_PASSWORD)
        
        print "Waiting %s seconds for nodes to become ready" % (settings.HADOOP_WAIT_TIME)
        time.sleep(settings.HADOOP_WAIT_TIME)
    
    def __generate_hosts_update_command(self):
        '''
        Generates a hosts update command
        '''
        
        hosts_file_update = [settings.SYSTEM_CLEAN_HOSTS_FILE]
        for host in self.__hosts:
            hosts_file_update.append("echo '" + host + settings.WHITESPACE + settings.SYSTEM_HOSTNAME_PREFIX \
                                      + remove_dots(host) + "' >> /etc/hosts")
        return hosts_file_update
        
    def prepare_environment(self):
        '''
        Prepares the system environment (updates hosts list, 
                                         sets hostname,
                                         apply urandom and ulimit fixes)
        '''
        
        hosts_file_update_command = self.__generate_hosts_update_command()
        hosts_dict = {}
        for host in self.__hosts:
            commands = [settings.SYSTEM_URANDOM_FIX, settings.SYSTEM_ULIMIT_FIX]
            commands.append("echo " + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(host) + " > /etc/hostname")
            commands.append("hostname -v " + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(host))
            commands.extend(hosts_file_update_command)
            hosts_dict.update({host: commands})
        
        self.sshClient.run_distinct_commands_on_hosts(hosts_dict, 
                                                      settings.SYSTEM_ROOT_USER_NAME, 
                                                      settings.SYSTEM_ROOT_USER_PASSWORD)
    def start(self):
        self.prepare_environment()

        if self.__storage_mode == "nfs":
            self.configure_slave_hosts_nfs()
        elif self.__storage_mode == "hdfs":
            self.configure_slave_hosts_hdfs()
        
        self.__configure_master_host()
        
    def configure_slave_hosts_nfs(self):
        logger.info("Preparing the following VMs with NFS: %s" % self.__hosts)
        commands = [settings.SYSTEM_KILL_JAVA,
                    settings.SYSTEM_CLEAN_TMP,
                    settings.HADOOP_DISABLE_HOST_KEY_CHECK,
                    settings.HADOOP_UPDATE_ENV]

        commands.append('''cat >''' + settings.HADOOP_INSTALL_DIR + '''/conf/mapred-site.xml <<EOF 
<?xml version="1.0"?> 
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>  
<configuration>
  <property> 
    <name>mapred.job.tracker</name> 
    <value>''' + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(self.master_host) + ''':8021</value> 
  </property> 

  <property>
    <name>mapred.child.java.opts</name>
    <value>-Xmx''' + settings.HADOOP_XMX_SIZE + '''m -Xmn''' + settings.HADOOP_XMN_SIZE + '''m</value>
  </property>

  <property>
    <name>mapred.tasktracker.map.tasks.maximum</name>
    <value>''' + settings.HADOOP_MAX_NUMBER_OF_MAP_SLOTS + '''</value>
  </property>

  <property>
    <name>mapred.tasktracker.reduce.tasks.maximum</name>
    <value>''' + settings.HADOOP_MAX_NUMBER_OF_REDUCE_SLOTS + '''</value>
  </property>
  
  <property>
      <name>mapred.local.dir</name>
      <value>''' + settings.HADOOP_MAPRED_LOCAL_DIR + '''</value>
   </property>
   
  <property>
      <name>mapred.system.dir</name>
      <value>''' + settings.HADOOP_MAPRED_SYSTEM_DIR + '''</value>
   </property>
   
  <property>
      <name>mapred.temp.dir</name>
      <value>''' + settings.HADOOP_MAPRED_TEMP_DIR + '''</value>
   </property>
</configuration> 
EOF''')

        commands.append('''cat >''' + settings.HADOOP_INSTALL_DIR + '''/conf/core-site.xml <<EOF 
<?xml version="1.0"?> 
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>  
<configuration> 
  <property> 
    <name>fs.default.name</name> 
    <value>file:///</value> 
  </property>

  <property> 
    <name>io.file.buffer.size</name> 
    <value>''' + settings.HADOOP_IO_FILE_BUFFER_SIZE + '''</value> 
  </property>
</configuration>
EOF''')   
            
        self.sshClient.run_same_commands_on_hosts(self.__hosts, 
                                                  commands,
                                                  settings.SYSTEM_HADOOP_USER_NAME, 
                                                  settings.SYSTEM_HADOOP_USER_PASSWORD)
                                                  
    def configure_slave_hosts_hdfs(self):
        logger.info("Preparing the following VMs with HDFS: %s" % self.__hosts)
        commands = [settings.SYSTEM_KILL_JAVA,
                    settings.SYSTEM_CLEAN_TMP,
                    settings.HADOOP_DISABLE_HOST_KEY_CHECK,
                    settings.HADOOP_UPDATE_ENV]

        commands.append('''cat >''' + settings.HADOOP_INSTALL_DIR + '''/conf/hdfs-site.xml <<EOF 
<?xml version="1.0"?> 
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>  
<configuration> 
    <property> 
        <name>dfs.block.size</name> 
        <value>''' + settings.HADOOP_BLOCK_SIZE + '''</value> 
        <final>true</final>
    </property>

    <property>
       <name>dfs.datanode.max.xcievers</name>
       <value>''' + settings.HADOOP_MAX_XCIEVERS + '''</value>
    </property>
      
    <property> 
        <name>dfs.replication</name> 
        <value>''' + settings.HADOOP_RELICATION_FACTOR + '''</value> 
        <final>true</final>
    </property>
</configuration>
EOF''')

        commands.append('''cat >''' + settings.HADOOP_INSTALL_DIR + '''/conf/mapred-site.xml <<EOF 
<?xml version="1.0"?> 
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>  
<configuration>
  <property> 
    <name>mapred.job.tracker</name> 
    <value>''' + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(self.master_host) + ''':8021</value> 
  </property> 

  <property>
    <name>mapred.child.java.opts</name>
    <value>-Xmx''' + settings.HADOOP_XMX_SIZE + '''m -Xmn''' + settings.HADOOP_XMN_SIZE + '''m</value>
  </property>

  <property>
    <name>mapred.tasktracker.map.tasks.maximum</name>
    <value>''' + settings.HADOOP_MAX_NUMBER_OF_MAP_SLOTS + '''</value>
  </property>

  <property>
    <name>mapred.tasktracker.reduce.tasks.maximum</name>
    <value>''' + settings.HADOOP_MAX_NUMBER_OF_REDUCE_SLOTS + '''</value>
  </property>
</configuration> 
EOF''')

        commands.append('''cat >''' + settings.HADOOP_INSTALL_DIR + '''/conf/core-site.xml <<EOF 
<?xml version="1.0"?> 
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>  
<configuration> 
  <property> 
    <name>fs.default.name</name> 
    <value>hdfs://''' + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(self.master_host) + '''</value> 
  </property>
  
  <property> 
    <name>io.file.buffer.size</name> 
    <value>hdfs://''' + settings.HADOOP_IO_FILE_BUFFER_SIZE + '''</value> 
  </property>
</configuration>
EOF''')   
            
        self.sshClient.run_same_commands_on_hosts(self.__hosts, 
                                                  commands,
                                                  settings.SYSTEM_HADOOP_USER_NAME, 
                                                  settings.SYSTEM_HADOOP_USER_PASSWORD)

class HadoopConfigureSeparateData(HadoopConfigureNormal):
        '''
        Custon Hadoop configuration
        '''
      
        def __init__(self, master_host, data_hosts, compute_hosts, storage_mode):
            self.__data_hosts = data_hosts
            self.__compute_hosts = compute_hosts
            hosts = data_hosts + compute_hosts            
            super(HadoopConfigureSeparateData, self).__init__(master_host, hosts, storage_mode)
        
        def __start_data_hosts(self):
            commands = [settings.HADOOP_CLEAN_SLAVES_FILE]
            for data_host in self.__data_hosts:
                commands.append("echo " + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(data_host) + " >> " + \
                                 settings.HADOOP_SLAVES_FILE)
            
            commands.append(settings.HADOOP_FORMAT_DFS)
            commands.append(settings.HADOOP_START_DFS)
            self.sshClient.run_commands_on_host(self.master_host, 
                                                commands, 
                                                settings.SYSTEM_HADOOP_USER_NAME, 
                                                settings.SYSTEM_HADOOP_USER_PASSWORD)
            
            print "Waiting %s seconds for nodes to become ready" % (settings.HADOOP_WAIT_TIME)
            time.sleep(settings.HADOOP_WAIT_TIME)
            
        
        def __start_task_trackers(self):
            commands = [settings.HADOOP_CLEAN_SLAVES_FILE,
                        "echo " + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(self.master_host) + " > " \
                        + settings.HADOOP_MASTER_FILE]
            
            for compute_host in self.__compute_hosts:        
                commands.append("echo " + settings.SYSTEM_HOSTNAME_PREFIX + remove_dots(compute_host) + " >> " + \
                                 settings.HADOOP_SLAVES_FILE)
            
            commands.append(settings.HADOOP_START_MAPRED)
            self.sshClient.run_commands_on_host(self.master_host, 
                                                commands, 
                                                settings.SYSTEM_HADOOP_USER_NAME, 
                                                settings.SYSTEM_HADOOP_USER_PASSWORD)
        def start(self):
            self.prepare_environment()
            self.configure_slave_hosts_hdfs()
            self.__configure_master_host()
            
        def __configure_master_host(self):
            self.__start_task_trackers()
            self.__start_data_hosts()
