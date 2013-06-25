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

import logging

from config import settings
from utils.ssh_client import SSHClient

logger = logging.getLogger(__name__)

class HadoopBenchmark(object):
    '''
    Hadoop MapReduce benchmarks
    '''
    
    def __init__(self, master):
        '''
        Constructor
        ''' 
        self.__master = master
        self.__sshClient = SSHClient()

    def __read_maps_reduces(self):
        number_of_maps = raw_input("Number of maps:")
        number_of_reduces = raw_input("Numer of reduces:")  
        return number_of_maps, number_of_reduces
            
    def __read_input_census_and_wiki(self):
        '''
        Reads the input
        '''
        test_number = raw_input("Test number(0 -> read=write, 1 -> read>write, 2 -> read<write):")
        number_of_maps, number_of_reduces = self.__read_maps_reduces()
        return test_number, number_of_maps, number_of_reduces
            
    def dfsio(self):        
        number_of_files = raw_input("Number of files:")
        file_size = raw_input("File size: ")
        logger.info("Write test started")
        write_command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_TEST_BENCHMARK \
                        + "TestDFSIO -write -nrFiles " + number_of_files + " -fileSize " + file_size
        
        logger.info("Read test started")
        read_command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_TEST_BENCHMARK \
                       + "TestDFSIO -read -nrFiles " + number_of_files + " -fileSize " + file_size
        
        logger.info("Cleaning")
        clean_command = settings.HADOOP_START_TEST_BENCHMARK + "TestDFSIO -clean"
        return [write_command, read_command, clean_command]

    def dfsthroughput(self):        
        start_command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_TEST_BENCHMARK + "dfsthroughput"        
        clean_command = settings.HADOOP_START_TEST_BENCHMARK + "dfsthroughput -clean"
        return [start_command, clean_command] 
    
    def mrbench(self):   
        number_of_runs = raw_input("Number of runs:")
        command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_TEST_BENCHMARK \
                  + "mrbench -numRuns " + number_of_runs 
        return [command]      

    def nnbench(self):   
        logger.info("nnbench")
        operation = raw_input("Operation (create_write/open_read/rename/delete):")
        number_of_maps, number_of_reduces = self.__read_maps_reduces()
        number_of_files = raw_input("Number of files:")
        
        command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_TEST_BENCHMARK + "nnbench -operation " + operation + " -maps " \
                  + number_of_maps + " -reduces " + number_of_reduces + " -blockSize 1 -bytesToWrite 0 -numberOfFiles "\
                  + number_of_files + " -replicationFactorPerFile 3 -readFileAfterOpen true"
        return [command] 
     
    def pi(self):
        number_of_maps = raw_input("Number of maps:")
        number_of_samples = raw_input("Numer of samples:")       
        command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_EXAMPLE_BENCHMARK + "pi " + number_of_maps + \
                  settings.WHITESPACE + number_of_samples
        return [command] 
        
    def __get_number_of_maps_reduces_parameter(self):
        '''
        Computes number of maps, reduces parameter setting
        '''
        number_of_maps, number_of_reduces = self.__read_maps_reduces()
        return settings.HADOOP_SET_NUMBER_OF_MAPS + number_of_maps + settings.WHITESPACE \
               + settings.HADOOP_SET_NUMBER_OF_REDUCES + number_of_reduces + settings.WHITESPACE
               
    def teragen(self):
        number_of_rows = raw_input("Number of 100 byte rows:")
        number_of_maps = raw_input("Number of maps:")
        teragen_command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_EXAMPLE_BENCHMARK \
                          + "teragen" + settings.WHITESPACE +  settings.HADOOP_SET_NUMBER_OF_MAPS + number_of_maps \
                          + settings.WHITESPACE + number_of_rows + settings.WHITESPACE + settings.TERAGEN_LOCATION_INPUT
        return [settings.TERAGEN_CLEAN_INPUT, teragen_command]
                
    def terasort(self):
        maps_reduces_parameter = self.__get_number_of_maps_reduces_parameter()
        terasort_command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_EXAMPLE_BENCHMARK \
                          + "terasort" + settings.WHITESPACE + maps_reduces_parameter \
                          + settings.WHITESPACE + settings.TERAGEN_LOCATION_INPUT \
                          + settings.WHITESPACE + settings.TERAGEN_LOCATION_OUTPUT
        return [settings.TERAGEN_CLEAN_OUTPUT, terasort_command]    

    def teravalidate(self):
        maps_reduces_parameter = self.__get_number_of_maps_reduces_parameter()
        teravalidate_command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_EXAMPLE_BENCHMARK \
                               + "teravalidate" + settings.WHITESPACE + maps_reduces_parameter \
                               + settings.WHITESPACE + settings.TERAGEN_LOCATION_OUTPUT \
                               + settings.WHITESPACE + settings.TERAGEN_LOCATION_VALIDATE
        return [settings.TERAGEN_CLEAN_VALIDATE, teravalidate_command]    
        
    def census_data(self):
        data_source_directory = raw_input("Input data file/directory on NAS:")
        mkdir_command = settings.HADOOP_MKDIR_COMMAND + settings.CENSUSPROC_LOCATION_INPUT
        move_command = settings.SYSTEM_TIME_COMMAND  + settings.HADOOP_COPY_FROM_LOCAL \
                       + data_source_directory + settings.WHITESPACE + settings.CENSUSPROC_LOCATION_INPUT
        return [settings.CENSUSPROC_CLEAN_INPUT, mkdir_command, move_command]
        
    def census_bench(self):
        test_number, number_of_maps, number_of_reducers = self.__read_input_census_and_wiki()
        start_command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_COMMAND + settings.CENSUSPROC_LOCATION_BIN \
                        + settings.WHITESPACE + test_number + settings.WHITESPACE + number_of_maps + settings.WHITESPACE \
                        + number_of_reducers + settings.WHITESPACE + settings.CENSUSPROC_LOCATION_INPUT + settings.WHITESPACE \
                        +settings.CENSUSPROC_LOCATION_OUTPUT
        return [settings.CENSUSPROC_CLEAN_OUTPUT, start_command]

    def wikipedia_data(self):
        data_source_directory = raw_input("Input data file/directory on NAS: ")
        mkdir_command = settings.HADOOP_MKDIR_COMMAND + settings.WIKIPROC_LOCATION_INPUT
        move_command = settings.SYSTEM_TIME_COMMAND + settings.WHITESPACE + settings.HADOOP_COPY_FROM_LOCAL \
                       + data_source_directory + settings.WHITESPACE + settings.WIKIPROC_LOCATION_INPUT
        return [settings.WIKIPROC_CLEAN_INPUT, mkdir_command, move_command]
    
    def wikipedia_bench(self):
        test_number, number_of_maps, number_of_reducers = self.__read_input_census_and_wiki()
        start_command = settings.SYSTEM_TIME_COMMAND + settings.HADOOP_START_COMMAND + settings.WIKIPROC_LOCATION_BIN \
                        + settings.WHITESPACE + test_number + settings.WHITESPACE + number_of_maps + settings.WHITESPACE \
                        + number_of_reducers + settings.WHITESPACE + settings.WIKIPROC_LOCATION_INPUT + settings.WHITESPACE \
                        + settings.WIKIPROC_LOCATION_OUTPUT
        return [settings.WIKIPROC_CLEAN_OUTPUT, start_command]

    def run_benchmark(self, name):
        logger.debug("Starting %s benchmark on master node: %s" %(name, self.__master))

        benchmarks = {
         "dfsio": self.dfsio,
         "dfsthroughput": self.dfsthroughput,
         "mrbench": self.mrbench,
         "nnbench": self.nnbench,
         "pi": self.pi,
         "teragen": self.teragen,
         "terasort": self.terasort,
         "teravalidate": self.teravalidate,
         "censusdata": self.census_data,
         "censusbench": self.census_bench,
         "wikidata": self.wikipedia_data,
         "wikibench": self.wikipedia_bench
        }
    
        benchmark = benchmarks[name]
        commands = benchmark()
        
        self.__sshClient.run_commands_on_host(self.__master, 
                                              commands, 
                                              settings.SYSTEM_HADOOP_USER_NAME, 
                                              settings.SYSTEM_HADOOP_USER_PASSWORD)
