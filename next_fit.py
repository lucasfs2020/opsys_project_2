# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:51:16 2019

@author: standl
"""

import memory_process
import sys

def check_free(m_table, process_id, size):
    cont_free = 0
    max_cont = 0
    total_free = 0
    consecutive = 0
    fits = 0
    start = []
    end = []
    
    for i in range(len(m_table)):
        for j in range(len(m_table[i])):
            if (m_table[i][j] == "."):
                total_free += 1;
                if consecutive == 0:
                    consecutive = 1
                    cont_free += 1
                    start = [i, j]
                    end = []
                elif consecutive == 1:
                    cont_free += 1
                    if (cont_free >= max_cont):
                        max_cont = cont_free
                    if cont_free >= size:
                        end = [i, j]
                        return (start, end)
            else:
                consecutive = 0
                cont_free = 0
                end = [i, j]
    if (end == []):
        end = [len(m_table)-1, len(m_table[0])-1]
    
    return(start, end)
    
    
    
def run_nf(memory):
    check_free(m_table)