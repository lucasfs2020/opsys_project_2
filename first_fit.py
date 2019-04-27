# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:50:46 2019

@author: standl
"""

import memory_process
import sys
import math
import numpy as np

def check_free(m_table, process_id, size):
    cont_free = 0
    max_cont = 0
    total_free = 0
    consecutive = 0
    fit = 0
    start = []
    end = []
    
    for i in range(len(m_table)):
        if (m_table[i] == "."):
            total_free += 1;
            if consecutive == 0:
                consecutive = 1
                cont_free += 1
                start = i
                end = 0
            elif consecutive == 1:
                cont_free += 1
                if process_id == "A":
                    print("here")
                    print(cont_free)
                if (cont_free >= max_cont):
                    max_cont = cont_free
                if cont_free >= size:
                    end = i
                    fit = 1
                    return (start, end, total_free, fit)
        elif (m_table[i] != "."):
            consecutive = 0
            end = i
            if cont_free >= size:
                return (start, end , total_free, fit)
            else:
                cont_free = 0
    
    return (start, end, total_free, fit)
    
def mem_sec(memory_table):
    start = 0
    end = 0
    sections = []
    current_letter = ""
    section_on = 0
    for i in range(len(memory_table)):
        if (memory_table[i] != "."):
            if section_on == 0:
                start = i
                current_letter = memory_table[i]
                section_on = 1
        elif (memory_table[i] == "."):
            if (section_on == 1):
                end = i
                sections.append([current_letter, start, end])
                section_on = 0
                current_letter = ""
    return sections

def defrag(memory_table):
    sections = mem_sec(memory_table)
    sections[0][1] -= sections[0][1]
    sections[0][2] = sections[0][2] - sections[0][1]
    total_difference = sections[0][1]
    print(len(sections))
    if len(sections) > 1:
        for i in range(1, len(sections)):
            prior_end = sections[i-1][2]
            current_start = sections[i][1]
            difference = current_start - prior_end
            sections[i][1] -= difference
            sections[i][2] -= difference
            total_difference += difference
    
    new_table = np.chararray((len(memory_table)), unicode = True)
    new_table[:] = "."    
    for i in range(len(sections)):
        letter = sections[i][0]
        start = sections[i][1]
        end = sections[i][2]
        new_table[start:end] = letter
    
    return new_table, difference

def find_arrivals(mem_proc_arr, time):
    current_arrivals = []
    for proc in mem_proc_arr:
        if proc.arrival_time_1 == time:
            current_arrivals.append(proc)
        if proc.second_run == True:
            if proc.arrival_time_2 == time:
                current_arrivals.append(proc)
    
    if not current_arrivals:
        return 0
    
    current_arrivals.sort(key=lambda x: x.pid)
    
    return current_arrivals

def print_table(table, frames_pl, total_f):
    lines = math.ceil(total_f/frames_pl)
    
    print("="*frames_pl)
    curr_line = 0
    
    for i in range(total_f):
        print(table[i], end = "")
        if ((i+1)%frames_pl == 0):
            curr_line += 1
            if (curr_line != lines):
                print()
    print()
    print("="*frames_pl)

def run_ff(memory, mem_proc_arr, fpl, tf, tmm):
    
    running = []
    
    time = 0
    
    print("time 0ms: simulator started ()")
    
    while (mem_proc_arr):
        current_arrival = find_arrivals(mem_proc_arr, time)
        
        start = 0
        end = 0
        
        if running:
            marked = []
            for run_proc in running:
                if run_proc[1] == time:
                    marked.append(run_proc)
            
            for mark in marked:
                print("time %dms: Process %s removed" % (time, mark[0].pid))
                memory[mark[2]:mark[3]+1] = "."
                #print(memory)
                print_table(memory, fpl, tf)
                print(mark[0].runs)
                running.remove(mark)
                if mark[0].runs == 1 and mark[0].second_run == 0:
                    #print(mark[0])
                    #print(running[0])
                    mem_proc_arr.remove(mark[0])
                elif mark[0].runs == 2 and mark[0].second_run == 1:
                    mem_proc_arr.remove(mark[0])
                    
        if (current_arrival != 0):
            for i in range(len(current_arrival)):
                if current_arrival[i].runs == 1:
                    print(current_arrival[i].pid)
                
                start, end, total_free, fit = check_free(memory, current_arrival[i].pid, current_arrival[i].p_mem)
                
                print("time %dms: Process %s (requires %d frames)" % (time, current_arrival[i].pid, current_arrival[i].p_mem))
                if fit == 1:
                    current_arrival[i].runs += 1
                    print("time %dms: Placed process %s"%(time, current_arrival[i].pid))
                    if current_arrival[0].pid == "A":
                        print(start, end)
                    memory[start:end+1] = current_arrival[i].pid
                    print_table(memory, fpl, tf)
                    end_time = 0
                    if current_arrival[i].runs == 1:
                        end_time = current_arrival[i].arrival_time_1+current_arrival[i].run_time_1
                    elif current_arrival[i].runs == 2:
                        end_time = current_arrival[i].arrival_time_2+current_arrival[i].run_time_2
                    running.append([current_arrival[i], end_time, start, end])
                elif total_free > current_arrival[i].p_mem:
                    memory, frames = defrag(memory)
                    time_loss = frames*tmm
                    time += time_loss
                    
                    print(memory)
                    print(running)
                    break
                elif total_free < current_arrival[i].p_mem:
                    print("time %dms: Cannot place process %s -- skipped!" % (time, current_arrival[i].pid))
                    current_arrival[i].runs += 1
                    if current_arrival[i].runs == 1 and current_arrival[i].second_run == 0:
                        mem_proc_arr.remove(current_arrival[i])
                    elif current_arrival[i].runs == 2 and current_arrival[i].second_run == 1:
                        mem_proc_arr.remove(current_arrival[i])
                
        
        if mem_proc_arr:
            time += 1
    
    print("time %dms: Simulator ended (Contiguous -- First-Fit)"% time)
    