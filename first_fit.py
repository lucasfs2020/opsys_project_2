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
            elif (memory_table[i] != current_letter):
                #print("here")
                if section_on == 1:
                    end = i
                    sections.append([current_letter, start, end])
                    start = i+1
                    current_letter = memory_table[i]
        elif (memory_table[i] == "."):
            if (section_on == 1):
                end = i
                sections.append([current_letter, start, end])
                section_on = 0
                current_letter = ""
    return sections

def frame_calc(old_table, new_table):
    old_sec = mem_sec(old_table)
    new_sec = mem_sec(new_table)
    
    frames_moved = 0
    
    for i in range(len(old_sec)):
        if old_sec[i][1] != new_sec[i][1]:
            frames_moved += old_sec[i][2]-old_sec[i][1]
            
    return frames_moved + 1
    
def defrag(memory_table):
    sections = mem_sec(memory_table)
    frames = 0
    sections[0][1] -= sections[0][1]
    sections[0][2] = sections[0][2] - sections[0][1]
    difference = sections[0][2] - sections[0][1]
    #print(difference)
    #print(sections)
    #print(len(sections))
    if len(sections) > 1:
        for i in range(1, len(sections)):
            prior_end = sections[i-1][2]
            current_start = sections[i][1]
            difference = current_start - prior_end
            sections[i][1] -= difference
            sections[i][2] -= difference
    
    new_table = np.chararray((len(memory_table)), unicode = True)
    new_table[:] = "."    
    for i in range(len(sections)):
        letter = sections[i][0]
        start = sections[i][1]
        end = sections[i][2]
        frames += (end-start)
        new_table[start:end+1] = letter
    
    frames = frame_calc(memory_table, new_table)
    
    return new_table, frames

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

def reset_run(memory, run_procs, time, time_diff):
    new_t = mem_sec(memory)
    #print(new_t)
    for proc in run_procs:
        for new_proc in new_t:
            name = new_proc[0]
            start = new_proc[1]
            end = new_proc[2]
            if name == proc[0].pid:
                proc[0].end_time += time_diff
                proc[1] = start
                proc[2] = end
    
    return run_procs

def update_time(procs, time_diff, time):
    for process in procs:
        if process.runs == 0:
            if process.arrival_time_1 > time and process.second_run == 0:
                process.arrival_time_1 += time_diff
            elif process.arrival_time_1 > time and procs.second_run == 1:
                process.arrival_time_1 += time_diff
                process.arrival_time_2 += time_diff
        elif process.runs == 1 and process.second_run == 1:
            if process.arrival_time_2 > time:
                process.arrival_time_2 += time_diff
            
    return procs

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
                if run_proc[0].end_time == time:
                    marked.append(run_proc)
            
            for mark in marked:
                print("time %dms: Process %s removed" % (time, mark[0].pid))
                memory[mark[1]:mark[2]+1] = "."
                #print(memory)
                print_table(memory, fpl, tf)
                #print(mark[0].runs)
                running.remove(mark)
                if mark[0].runs == 1 and mark[0].second_run == 0:
                    #print(mark[0])
                    #print(running[0])
                    mem_proc_arr.remove(mark[0])
                elif mark[0].runs == 2 and mark[0].second_run == 1:
                    mem_proc_arr.remove(mark[0])
                    
        if (current_arrival != 0):
            for i in range(len(current_arrival)):
                #if current_arrival[i].runs == 1:
                    #print(current_arrival[i].pid)
                
                start, end, total_free, fit = check_free(memory, current_arrival[i].pid, current_arrival[i].p_mem)
                
                print("time %dms: Process %s (requires %d frames)" % (time, current_arrival[i].pid, current_arrival[i].p_mem))
                if fit == 1:
                    current_arrival[i].runs += 1
                    print("time %dms: Placed process %s"%(time, current_arrival[i].pid))
                    #if current_arrival[0].pid == "A":
                        #print(start, end)
                    memory[start:end+1] = current_arrival[i].pid
                    print_table(memory, fpl, tf)
                    end_time = 0
                    if current_arrival[i].runs == 1:
                        print(current_arrival[i].pid)
                        print(current_arrival[i].arrival_time_1)
                        print(current_arrival[i].run_time_1)
                        current_arrival[i].end_time = current_arrival[i].arrival_time_1+current_arrival[i].run_time_1
                    elif current_arrival[i].runs == 2:
                        current_arrival[i].end_time = current_arrival[i].arrival_time_2+current_arrival[i].run_time_2
                    running.append([current_arrival[i], start, end])
                elif total_free > current_arrival[i].p_mem:
                    #print("Here at time %d\n"%time)
                    print("Cannot place, beginning defragmentation")
                    memory, frames = defrag(memory)
                    print(frames)
                    time_loss = frames*tmm
                    time += time_loss
                    print("time: %d, placed process"%time)
                    running = reset_run(memory, running, time, time_loss)
                    mem_proc_arr = update_time(mem_proc_arr, time_loss, time)
                    start, end, total_free, fit = check_free(memory, current_arrival[i].pid, current_arrival[i].p_mem)
                    memory[start:end+1] = current_arrival[i].pid
                    if current_arrival[i].runs == 1:
                        end_time = current_arrival[i].arrival_time_1+current_arrival[i].run_time_1
                    elif current_arrival[i].runs == 2:
                        end_time = current_arrival[i].arrival_time_2+current_arrival[i].run_time_2
                    running.append([current_arrival[i], end_time, start, end])
                    print_table(memory, fpl, tf)
                    #print(time)
                    
                elif total_free < current_arrival[i].p_mem:
                    print("time %dms: Cannot place process %s -- skipped!" % (time, current_arrival[i].pid))
                    current_arrival[i].runs += 1
                    if current_arrival[i].runs == 1 and current_arrival[i].second_run == 0:
                        mem_proc_arr.remove(current_arrival[i])
                    elif current_arrival[i].runs == 2 and current_arrival[i].second_run == 1:
                        mem_proc_arr.remove(current_arrival[i])

        if mem_proc_arr:
            time += 1
        if time == 2815:
            for proc in mem_proc_arr:
                print(proc.pid)
    print("time %dms: Simulator ended (Contiguous -- First-Fit)"% time)
    