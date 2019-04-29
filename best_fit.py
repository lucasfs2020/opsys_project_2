'''
best_fit

For the best-fit algorithm, process X is placed in the smallest free 
partition available in which process X fits. If a \tie" occurs, 
use the free partition closer to the \top" of memory.

For all of these placement algorithms, the memory scan covers the entire 
memory. If necessary (i.e., if the scan hits the \bottom" of memory), 
the scan continues from the \top" of memory. And if no suitable free 
partition is available, then an out-of-memory error occurs, at which 
point defragmentation might occur
'''
import memory_process
import sys
import math
import numpy as np



'''
	find_arrivals

	goes through all processes to check if any have arrived yet
	updates and returns the current_arrivals array
	params:
		mem_proc_arr : the array of all processes
		time : the current time
		current_arrivals : the array of processes that have arrived
	return:
		current_arrivals
		arrival : 0 if nothing arrived, 1 if something arrived
'''
def find_arrivals(mem_proc_arr, time):
	arrival = 0
	current_arrivals = []
	#go through all processes
	for proc in mem_proc_arr:
		#check if the first process has arrived yet
		if proc.arrival_time_1 == time:
			current_arrivals.append(proc)
			arrival = 1
		#check if it has a second process
		if proc.second_run == True:
			#check if the second process has arrived yet
			if proc.arrival_time_2 == time:
				current_arrivals.append(proc)
				arrival = 1
	#sort the arrivals by their process ids
	current_arrivals.sort(key=lambda x: x.pid)
	return current_arrivals, arrival




'''
	print_table

	function that prints the table in the correct format
	params:
		table : the table
		frames_pl : frames per line
		total_f : total frames
'''
def print_table(table, frames_pl, total_f):
    lines = math.ceil(total_f/frames_pl)
    print("=" * frames_pl)
    curr_line = 0
    for i in range(total_f):
        print(table[i], end = "")
        if ((i + 1) % frames_pl == 0):
            curr_line += 1
            if (curr_line != lines):
                print()
    print()
    print("=" * frames_pl)





'''
	get_free_space

	function to return the number of free blocks in the current open
	memory segment
	params:
		m_table : the memory table
		size : the number of frames the process takes up in m_table
	return:
		smallest_start : the starting index of the chosen segment 
		smallest_end : the end index of the chosen segment
		total_free : the amount of total free blocks
'''
def get_free_space(m_table, size):
	#smallest_section keeps track of the smallest free section
	smallest_section = len(m_table)+1
	#the start and end of the smallest section
	smallest_start = -1
	smallest_end = -1
	#keep track of the start and end of the current free section
	start = -1
	end = -1
	#keep track of how many spaces are free
	total_free = 0
	i = 0
	#go through to find all spaces with "."
	while (i < len(m_table)):
		if (m_table[i] == "."):
			start = i
			while (m_table[i] == "."):
				if (i+1 < len(m_table)):
					total_free += 1
					i += 1
				else:
					break
			end = i 
			#see if the process fits here
			if (end-start) >= size:
				#only reset if it is less then because a tie goes to the earlier section
				if (end-start) < smallest_section:
					smallest_section = end-start
					smallest_start = start
					smallest_end = start+size-1
		i += 1

	return smallest_start, smallest_end, total_free





'''
	defrag

	a function to move the processes in the memory table to condense
	all processes currently in the table and free up space at the bottom 
	of said table (the end of the array)
	params:
		m_table : the memory table that holds the processes
		move_time : the time it takes to move one frame of a process
	return:
		m_table : updated
		defrag_time : the total time it took to fix the table
		frames_moved : how many total frames were moved 
		frames : an array of the pids of the moved processes
'''
def defrag(m_table, move_time, tf):
	#the time it took to defragment
	defrag_time = 0
	#the number of total frames moved
	frames_moved = 0
	#the array of pids that were moved
	frames = []
	#the index of the first "."
	first_pd_arr = np.where(m_table == ".")
	#print(first_pd_arr)
	first_pd = first_pd_arr[0][0]
	#print("   first period index: %d" %first_pd)
	#count the number of "."s
	pd_count = 0
	#temp_arr will keep track of all the process ids
	temp_arr = []
	#going through all the first processes that dont move in the array
	if first_pd != 0:
		k = 0
		while k < first_pd:
			temp_arr.append(m_table[k])
			k += 1

	#go through the rest of the m_table
	for i in range(first_pd, len(m_table)):
		#we do not count the empty "." blocks in the calculations
		if (m_table[i] != "."):
			#so m_table[i] is part of a process that needs to move
			frames_moved += 1
			#append the pid since it will need to be printed later
			frames.append(m_table[i])
			temp_arr.append(m_table[i])
		else:
			#count all the empty blocks
			pd_count += 1

	defrag_time = frames_moved * move_time

	#fix memory 
	#I create a new memory table so I can refil it with temp_arr pids
	new_m_table = np.chararray((tf), unicode = True)
	new_m_table[:] = "."
	length = len(temp_arr)
	i = 0
	while (i < length):
		new_m_table[i] = temp_arr[i]
		i += 1
	#get rid of the duplicate pids by making the list a dict then back to a list
	frames = list(dict.fromkeys(frames))

	return new_m_table, defrag_time, frames_moved, frames






'''
	run_bf

	the method to be called from the main file, calls all other methods
	in this file.
	params:
		memory : the first memory table
		mem_proc_arr :	the array of memory processes
		fpl : frames per line ?
		tf : total frames ?
		tmm : time memory moves
'''
def run_bf(memory, mem_proc_arr, fpl, tf, tmm):
	#need the time variable to keep track
	time = 0
	#store defrag time
	defrag_time = 0
	print("time 0ms: Simulator started (Contiguous -- Best-Fit)")
	#array to keep track of the running process
	running = []
	#first thing is we need to check if processes arrived
	#we can continue this for loop until we are out of processes
	while (mem_proc_arr):
		#current_arrivals, arrival = find_arrivals(mem_proc_arr, time, current_arrivals)
		current_arrivals, arrival = find_arrivals(mem_proc_arr, time)			
		#check if there is a process running
		if running:
			#finished processes go in the finished array
			finished = []
			#go through and see if any currently running processes are finished
			for proc in running:
				if proc[1] == time:
					finished.append(proc)
			#print out necessary info on the process
			for proc in finished:
				print("time %dms: Process %s removed" %(time+defrag_time, proc[0].pid))
				#when we defrag, these start and end indices saved in running will not be correct
				#so ill just refind the indices now
				letter = proc[0].pid
				g = 0
				new_start = -1
				new_end = -1
				while (g < len(memory)):
					if (memory[g] == letter):
						new_start = g
						while (memory[g] == letter):
							g += 1
						new_end = g
					g += 1
				#print("  new start : %d,     new end: %d" %(new_start, new_end))
				memory[new_start:new_end] = "."
				print_table(memory, fpl, tf)
				#remove the process from the running array
				running.remove(proc)
				#remove the process from the array of all processes if
				#the process only had one run and completed it
				if proc[0].runs == 1 and proc[0].second_run == 0:
					mem_proc_arr.remove(proc[0])
				#the process had two runs and completed them both
				elif proc[0].runs == 2 and proc[0].second_run == 1:
					mem_proc_arr.remove(proc[0])

		if arrival:
			#there was an arrival at the current time
			#go through the current arrivals
			for i in range(len(current_arrivals)):
				print("time %dms: Process %s arrived (requires %d frames)" %(time+defrag_time, current_arrivals[i].pid, current_arrivals[i].p_mem))
				#get the smallest start and smallest end for where to place the process
				smallest_start, smallest_end, total_free = get_free_space(memory, current_arrivals[i].p_mem)

				if (smallest_start != -1 and smallest_end != -1):
					#the process can be placed in a section as it is
					current_arrivals[i].runs += 1
					#placing the pid in the array
					memory[smallest_start:smallest_end+1] = current_arrivals[i].pid
					end_time = 0
					#calculate the end time based on if we are at the first or second process
					if current_arrivals[i].runs == 1:
						end_time = current_arrivals[i].arrival_time_1 + current_arrivals[i].run_time_1
					elif current_arrivals[i].runs == 2:
						end_time = current_arrivals[i].arrival_time_2 + current_arrivals[i].run_time_2
					#append the process to the running array
					running.append([current_arrivals[i], end_time, smallest_start, smallest_end])
					print("time %dms: Placed process %s:" %(time+defrag_time, current_arrivals[i].pid))
					print_table(memory, fpl, tf)
				elif total_free > current_arrivals[i].p_mem:
					#there was nowhere with enough space but altogether there is enough space to fit the proc
					#need to DEFRAGMENT
					print("time %dms: Cannot place process %s -- starting defragmentation" %(time+defrag_time, current_arrivals[i].pid))
					#memory will be the new memory array defragmented
					memory, new_defrag_time, frames_moved, frames = defrag(memory, tmm, tf)
					#can just add the time spent defragmenting to the current time spent defragmenting
					defrag_time += new_defrag_time
					#need a string of the processes moved by defragmentation
					str_moved_frames = ""
					for m in range(0,len(frames)-1):
						str_moved_frames += frames[m] + ", "
					str_moved_frames += frames[m+1]
					print("time %dms: Defragmentation complete (moved %d frames: %s)" %(time+defrag_time, frames_moved, str_moved_frames))
					#now we need to actually put the porcess into the memory array
					smallest_start, smallest_end, total_free = get_free_space(memory, current_arrivals[i].p_mem)
					#increment the run
					current_arrivals[i].runs += 1
					#put the process in the array
					memory[smallest_start:smallest_end+1] = current_arrivals[i].pid
					end_time = 0
					#calculate the end time
					if current_arrivals[i].runs == 1:
						end_time = current_arrivals[i].arrival_time_1 + current_arrivals[i].run_time_1
					elif current_arrivals[i].runs == 2:
						end_time = current_arrivals[i].arrival_time_2 + current_arrivals[i].run_time_2
					#print("     \n\nPROCESS %s HAS AN END TIME OF %d \n\n " %(current_arrivals[i].pid, end_time))
					running.append([current_arrivals[i], end_time, smallest_start, smallest_end])
					print("time %dms: Placed process %s:" %(time+defrag_time, current_arrivals[i].pid))
					print_table(memory, fpl, tf)
				elif total_free < current_arrivals[i].p_mem:
					#not enough room for the process even with defragmenting
					print("time %dms: Cannot place process %s -- skipped!" %(time+defrag_time, current_arrivals[i].pid))
					#increment runs even though the process was skipped
					current_arrivals[i].runs += 1
					if current_arrivals[i].runs == 1 and current_arrivals[i].second_run == 0:
						mem_proc_arr.remove(current_arrivals[i])
					elif current_arrivals[i].runs == 2 and current_arrivals[i].second_run == 1:
						mem_proc_arr.remove(current_arrivals[i])

		time += 1
	print("time %dms: Simulator ended (Contiguous -- Best-Fit)" %(time+defrag_time-1))

		
