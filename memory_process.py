# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 17:45:55 2019

@author: standl
"""

class Memory_Process:
    def __init__(self, pid, p_mem, arrival_time_1, run_time_1, arrival_time_2 = None, run_time_2 = None, second_run  = None):
        self.pid = pid
        self.p_mem = p_mem
        self.arrival_time_1 = arrival_time_1
        self.run_time_1 = run_time_1
        self.arrival_time_2 = arrival_time_2
        self.run_time_2 = run_time_2
        self.runs = 0
        self.second_run = second_run
        self.end_time = 0
        
    def print_vals(self):
        print("pid is " + self.pid)
        print("p_mem is " + str(self.p_mem))
        print("at1 is " + str(self.arrival_time_1))
        print("rt1 is " + str(self.run_time_1))
        print("at2 is " + str(self.arrival_time_2))
        print("rt2 is " + str(self.run_time_2))