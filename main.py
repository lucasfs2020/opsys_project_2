# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 17:12:46 2019

@author: standl
"""
import memory_process
import next_fit as nf
import sys
import numpy as np

def print_table(table, frames_pl, total_f):
    lines = int(total_f/frames_pl)
    
    print("="*frames_pl)
    
    for i in range(lines):
        for j in range(frames_pl):
            print(table[i*frames_pl+j], end = "")
        print()
    print("="*frames_pl)

if __name__ == '__main__':
    fpl = int(sys.argv[1])
    tf = int(sys.argv[2])
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
        
    lines = int(tf/fpl)
    print(lines)
        
    memory_table = np.chararray((tf), unicode = True)
    memory_table[:] = "."
    
    print(memory_table.shape)
    
    print(memory_table[0][0])
    
    print(memory_table)
    
    print_table(memory_table, fpl, tf)
    
    for proc in memory_process_arr:
        proc.print_vals()
    
    start, end = nf.check_free(memory_table, "A", 28)
    
    print(start[0])
    print(start[1])
    print(end[0])
    print(end[1])
    
    #memory_table[0, start[1]:end[1]] = "A"
    
    print_table(memory_table, fpl, tf)
    
    print(start, end)