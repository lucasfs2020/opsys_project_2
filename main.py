# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 17:12:46 2019

@author: standl
"""
import memory_process
import sys

if __name__ == '__main__':
    fpl = int(sys.argv[1])
    
    file_name = sys.argv[3]
    
    file = open(file_name, "r")
    memory_process_arr = []
    
    
    for line in file.readlines():
        line_arr = line.split()
        if len(line_arr) == 4:
            pid = line_arr[0]
            pmem = int(line_arr[1])
            time1 = line_arr[2].split("/")
            at1 = int(time1[0])
            rt1 = int(time1[1])
            time2 = line_arr[3].split("/")
            at2 = int(time2[0])
            rt2 = int(time2[1])
            new_process = memory_process.Memory_Process(pid, pmem, at1, rt1, at2, rt2)
            memory_process_arr.append(new_process)
        else:
            pid = line_arr[0]
            pmem = line_arr[1]
            time1 = line_arr[2].split("/")
            at1 = int(time1[0])
            rt1 = int(time1[1])
            new_process = memory_process.Memory_Process(pid, pmem, at1, rt1, None, None)
            memory_process_arr.append(new_process)
        
    
    for proc in memory_process_arr:
        proc.print_vals()