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

import argparse

from config.settings import logging
from storage.configure import StorageConfiguration
from config import settings
from hadoop.configure import HadoopConfigureNormal
from hadoop.configure import HadoopConfigureSeparateData
from hadoop.benchmark import HadoopBenchmark

logger = logging.getLogger(__name__)

def __storage(job_id, hosts):
    '''
    Configures the storage
    '''
    storage = StorageConfiguration(job_id, hosts)
    storage.configure_and_mount_nfs()
    
def __mapreduce_normal(master_node, slave_nodes):
    '''
    Configures normal MapReduce
    '''
    
    logger.info("Configuring Hadoop MapReduce on: %s" % slave_nodes)
    hadoop = HadoopConfigureNormal(master_node, slave_nodes, settings.HADOOP_STORAGE_MODE)
    hadoop.start()

def __mapreduce_separatedata(master_node, data_hosts, compute_hosts):
    '''
    Configures MapReduce with separate data
    '''
    
    logger.info("Configuring Hadoop MapReduce with %s data and %s compute hosts" % (data_hosts, compute_hosts))
    hadoop = HadoopConfigureSeparateData(master_node, data_hosts, compute_hosts, settings.HADOOP_STORAGE_MODE)
    hadoop.start()
    
def __benchmark(name, master_host):
    '''
    Benchmarks MapReduce
    '''
    
    logger.info("Starting to run the benchmark")
    benchmark = HadoopBenchmark(master_host)
    benchmark.run_benchmark(name) 
        
def __hosts_check(hosts):
    if len(hosts) < 2:
        logger.error("You need to specify atleast two hosts!")
        return False
        
    return True

if __name__ == '__main__':    
    parser  =  argparse.ArgumentParser(description="Snooze Hadoop MapReduce test suite")
    subparsers = parser.add_subparsers(title='available commands', 
                                       help='additional help',
                                       dest="subparser_name")
    # Storage command
    configure_parser = subparsers.add_parser('storage', help='NFS storage help')
    configure_parser.add_argument('--hosts', nargs="*", help="List of hosts (> 1)", required=True)
    configure_parser.add_argument('--job_id', help="Storage reservation job identifier", required=True)
    
    # Default configure command
    configure_parser = subparsers.add_parser('mapreduce_normal', help='MapReduce normal configuration help')
    configure_parser.add_argument('--master', help="Master node", required=True)
    configure_parser.add_argument('--slaves', nargs="*", help="List of slave nodes (> 1)", required=True)

    # Custom configure command
    configure_parser = subparsers.add_parser('mapreduce_separatedata', help='MapReduce separate data configuration help')
    configure_parser.add_argument('--master', help="Master node", required=True)
    configure_parser.add_argument('--data', nargs="*", help="List of data hosts", required=True)
    configure_parser.add_argument('--compute', nargs="*", help="List of compute hosts", required=True)
            
    # Run command
    benchmark_parser = subparsers.add_parser('benchmark', help='MapReduce benchmark help')
    benchmark_parser.add_argument('--name', help="Benchmark name (e.g. dfsio, dfsthroughput, mrbench, nnbench, pi, \
                                                  teragen, terasort, teravalidate, censusdata, censusbench, wikidata, wikibench)", \
                                                  required=True)
    benchmark_parser.add_argument('--master', help='Master host address', required=True)
    args = parser.parse_args()

    if args.subparser_name == 'storage':
        if __hosts_check(args.hosts):
            __storage(args.job_id, args.hosts)
        
    if args.subparser_name == 'mapreduce_normal':
        if __hosts_check(args.slaves):
            __mapreduce_normal(args.master, args.slaves)

    if args.subparser_name == 'mapreduce_separatedata':
            __mapreduce_separatedata(args.master, args.data, args.compute)
                
    if args.subparser_name == 'benchmark':
        __benchmark(args.name, args.master)
else:
    logger.error("Not allowed to be imported!")
