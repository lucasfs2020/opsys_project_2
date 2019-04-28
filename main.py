# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 17:12:46 2019

@author: standl
"""
import memory_process
import next_fit as nf
import first_fit as ff
import sys
import numpy as np
import math

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
    time_mem_move = int(sys.argv[4])
    
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
            second_run = True
            new_process = memory_process.Memory_Process(pid, pmem, at1, rt1, at2, rt2, second_run)
            memory_process_arr.append(new_process)
        else:
            pid = line_arr[0]
            pmem = int(line_arr[1])
            time1 = line_arr[2].split("/")
            at1 = int(time1[0])
            rt1 = int(time1[1])
            second_run = False
            new_process = memory_process.Memory_Process(pid, pmem, at1, rt1, None, None, second_run)
            memory_process_arr.append(new_process)
        
    lines = math.ceil(tf/fpl)
    print(lines)
        
    first_memory_table = np.chararray((tf), unicode = True)
    first_memory_table[:] = "."
    next_memory_table = np.chararray((tf), unicode = True)
    next_memory_table[:] = "."
    best_memory_table = np.chararray((tf), unicode = True)
    best_memory_table[:] = "."
    contiguous_memory_table = np.chararray((tf), unicode = True)
    contiguous_memory_table[:] = "."
    
    #print(first_memory_table.shape)
    
    #print(first_memory_table[0][0])
    
    #print(first_memory_table)
    
    #print_table(first_memory_table, fpl, tf)
    
    for proc in memory_process_arr:
        proc.print_vals()
    
    #start, end, total_free, fit = nf.check_free(memory_table, memory_process_arr[0].pid, memory_process_arr[0].p_mem)
    
    #current_arrival = ff.find_arrivals(memory_process_arr, 3)
    
    #print(current_arrival)
    
    #test_defrag = np.chararray((tf), unicode = True)
    #test_defrag[:] = "."
    
    #test_defrag[0:13] = "A"
    #test_defrag[15:20] = "B"
    #test_defrag[27:30] = "C"
    
    #running = [["B", 300, 15, 20], ["A", 200, 0, 13], ["C", 100, 27, 30]]
    
    #print(test_defrag)
    
    #defragged = ff.defrag(test_defrag)[0]
    
    #print(defragged)
    
    #print(ff.reset_run(defragged, running, 0, 50))
    
    ff.run_ff(first_memory_table, memory_process_arr, fpl, tf, time_mem_move)
    
    #memory_table[start:end] = "A"
    
    #print(start)
    #print(end)
    
    #memory_table[0, start[1]:end[1]] = "A"
    
    #print_table(memory_table, fpl, tf)
    
    #print(start, end)