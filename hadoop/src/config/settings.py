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

import logging.config

# Logging
logging.config.fileConfig('./hadoop/src/config/logging.conf')

# General
WHITESPACE = " "

# NFS server and parameters
NFS_STORAGE_SERVER = "storage5k.rennes.grid5000.fr"
NFS_MOUNT_DIRECTORY = "/mnt"

# G5K settings
G5K_USERNAME="efeller"
G5K_USERID="19067"

# System login information
SYSTEM_HOSTNAME_PREFIX = "host-"
SYSTEM_ROOT_USER_NAME = "root"
SYSTEM_ROOT_USER_PASSWORD = "root"
SYSTEM_HADOOP_USER_NAME = "hduser"
SYSTEM_HADOOP_USER_PASSWORD = "hadoop"
SYSTEM_HADOOP_GROUP = "hadoop"
SYSTEM_SSH_RETRY_COUNT = 3

# Other system settings
SYSTEM_HOSTS_FILE = "/etc/hosts"
SYSTEM_FSTAB_FILE = "/etc/fstab"
SYSTEM_TIME_COMMAND = "time" + WHITESPACE
SYSTEM_JAVA_INSTALL_DIR = "/usr/lib/jvm/java-6-openjdk-amd64"
SYSTEM_JAVA_HOME_ENV = "env JAVA_HOME=" + SYSTEM_JAVA_INSTALL_DIR + WHITESPACE
SYSTEM_KILL_JAVA = "pkill java || true"
SYSTEM_CLEAN_TMP = "rm -rf /tmp/hadoop* /tmp/hsperfdata_hadoop"
SYSTEM_CLEAN_HOSTS_FILE = "rm -f /etc/hosts"
SYSTEM_ULIMIT_FIX = "ulimit -n 64000"
SYSTEM_UMOUNT_NFS = "umount -lf" + WHITESPACE + NFS_MOUNT_DIRECTORY
SYSTEM_URANDOM_FIX = "mv /dev/random /dev/random.bak; ln -s /dev/urandom /dev/random"

# Hadoop general
HADOOP_VERSION = "1.0.4"
HADOOP_INSTALL_DIR = "/opt/hadoop"
HADOOP_CHMOD_FIX = "chmod -R 777" + WHITESPACE + HADOOP_INSTALL_DIR
HADOOP_DATA_DIRECTORY = "/data"
HADOOP_MASTER_FILE = HADOOP_INSTALL_DIR + "/conf/masters"
HADOOP_SLAVES_FILE = HADOOP_INSTALL_DIR + "/conf/slaves"
HADOOP_INSTALL_ENV = "env HADOOP_INSTALL=" + HADOOP_INSTALL_DIR + WHITESPACE
HADOOP_SYSTEM_ENV = SYSTEM_JAVA_HOME_ENV + HADOOP_INSTALL_ENV
HADOOP_BIN = HADOOP_SYSTEM_ENV + HADOOP_INSTALL_DIR + "/bin/hadoop" + WHITESPACE
HADOOP_CHOWN = "chown -R" + WHITESPACE + SYSTEM_HADOOP_USER_NAME + ":" + SYSTEM_HADOOP_GROUP + WHITESPACE + HADOOP_INSTALL_DIR
HADOOP_STORAGE_MODE="hdfs"
HADOOP_MAPRED_LOCAL_DIR="/tmp/hadoop/mapred/local"
HADOOP_MAPRED_SYSTEM_DIR="/mnt/hadoop/tmp/mapred/system"
HADOOP_MAPRED_TEMP_DIR="/mnt/hadoop/tmp/temp"
HADOOP_MAX_NUMBER_OF_MAP_SLOTS = "15" # depends on the cores
HADOOP_MAX_NUMBER_OF_REDUCE_SLOTS = "5"
HADOOP_RELICATION_FACTOR = "1"
HADOOP_XMX_SIZE="1024"
HADOOP_XMN_SIZE="400"
HADOOP_MAX_XCIEVERS="4096"
HADOOP_IO_FILE_BUFFER_SIZE="131072"
HADOOP_BLOCK_SIZE = "134217728"
HADOOP_WAIT_TIME = 20

# Hadoop prepares and cleanups
#HADOOP_DISABLE_HOST_KEY_CHECK = "echo 'StrictHostKeyChecking no' > ~hadoop/.ssh/config"
HADOOP_DISABLE_HOST_KEY_CHECK = "echo 'StrictHostKeyChecking no' > ~" + SYSTEM_HADOOP_USER_NAME + "/.ssh/config"
HADOOP_UPDATE_ENV = "echo 'export JAVA_HOME=" + SYSTEM_JAVA_INSTALL_DIR + "' >>" + WHITESPACE + \
                     HADOOP_INSTALL_DIR + "/conf/hadoop-env.sh"
HADOOP_CLEAN_SLAVES_FILE = "rm -f" + WHITESPACE + HADOOP_SLAVES_FILE 
                   
# Hadoop commands
HADOOP_START_COMMAND = HADOOP_BIN + "jar" + WHITESPACE
HADOOP_FS_COMMAND = HADOOP_BIN + "fs" + WHITESPACE
HADOOP_SET_NUMBER_OF_MAPS = "-Dmapred.map.tasks="
HADOOP_SET_NUMBER_OF_REDUCES = "-Dmapred.reduce.tasks="
HADOOP_FORMAT_DFS = HADOOP_BIN + "namenode -format"
HADOOP_START_TEST_BENCHMARK = HADOOP_START_COMMAND + HADOOP_INSTALL_DIR + "/hadoop-" + \
                              "test-"  + HADOOP_VERSION + ".jar" + WHITESPACE
HADOOP_START_EXAMPLE_BENCHMARK = HADOOP_START_COMMAND + HADOOP_INSTALL_DIR +"/hadoop-" + \
                                 "examples-" + HADOOP_VERSION + ".jar" + WHITESPACE
HADOOP_START_DFS = HADOOP_SYSTEM_ENV + HADOOP_INSTALL_DIR + "/bin/start-dfs.sh"
HADOOP_START_MAPRED = HADOOP_SYSTEM_ENV + HADOOP_INSTALL_DIR + "/bin/start-mapred.sh"
HADOOP_START_ALL_SERVICES = HADOOP_SYSTEM_ENV + HADOOP_INSTALL_DIR + "/bin/start-all.sh"
HADOOP_REMOVE_DATA_DIRECTORY = HADOOP_FS_COMMAND + "-rmr" + WHITESPACE
HADOOP_MKDIR_COMMAND = HADOOP_FS_COMMAND + "-mkdir" + WHITESPACE
HADOOP_COPY_FROM_LOCAL = HADOOP_FS_COMMAND + "-copyFromLocal" + WHITESPACE

# Custom apps (wikiproc and censusproc)
TERAGEN_LOCATION_INPUT = HADOOP_DATA_DIRECTORY + "/terasort-input"
TERAGEN_LOCATION_OUTPUT = HADOOP_DATA_DIRECTORY + "/terasort-output"
TERAGEN_LOCATION_VALIDATE = HADOOP_DATA_DIRECTORY + "/terasort-validate"
TERAGEN_CLEAN_INPUT = HADOOP_REMOVE_DATA_DIRECTORY + TERAGEN_LOCATION_INPUT
TERAGEN_CLEAN_OUTPUT = HADOOP_REMOVE_DATA_DIRECTORY + TERAGEN_LOCATION_OUTPUT
TERAGEN_CLEAN_VALIDATE = HADOOP_REMOVE_DATA_DIRECTORY + TERAGEN_LOCATION_VALIDATE
WIKIPROC_LOCATION_BIN = HADOOP_INSTALL_DIR + "/lbnl/wikiproc.jar"
WIKIPROC_LOCATION_INPUT =  HADOOP_DATA_DIRECTORY + "/wikipedia-input"
WIKIPROC_LOCATION_OUTPUT = HADOOP_DATA_DIRECTORY + "/wikipedia-output"
WIKIPROC_CLEAN_INPUT = HADOOP_REMOVE_DATA_DIRECTORY + WIKIPROC_LOCATION_INPUT
WIKIPROC_CLEAN_OUTPUT = HADOOP_REMOVE_DATA_DIRECTORY + WIKIPROC_LOCATION_OUTPUT
CENSUSPROC_LOCATION_BIN = HADOOP_INSTALL_DIR + "lbnl/censusproc.jar"
CENSUSPROC_LOCATION_INPUT = HADOOP_DATA_DIRECTORY + "/censusproc-input"
CENSUSPROC_LOCATION_OUTPUT = HADOOP_DATA_DIRECTORY + "/censusproc-output"
CENSUSPROC_CLEAN_INPUT = HADOOP_REMOVE_DATA_DIRECTORY + CENSUSPROC_LOCATION_INPUT
CENSUSPROC_CLEAN_OUTPUT = HADOOP_REMOVE_DATA_DIRECTORY + CENSUSPROC_LOCATION_OUTPUT
