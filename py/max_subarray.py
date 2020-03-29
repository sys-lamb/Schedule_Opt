#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:54:14 2020

@author: root
"""

import numpy as np
import random
# =============================================================================
# Brute force
# =============================================================================
def brute_force_max_subarray(my_array):
    max_sum = 0
    cur_sum = 0
    start_index = 0
    end_index = 0
    first_index = 0
    if len(my_array) == 1:
        return 0, 1, my_array[0]
    while first_index < len(my_array)+1:  
        second_index = first_index
        while second_index < len(my_array)+1:
            cur_sum = sum(my_array[first_index:second_index])   
            if cur_sum > max_sum:
                max_sum = cur_sum
                start_index = first_index
                end_index = second_index
            second_index += 1    
        first_index += 1
    return start_index, end_index, max_sum


# =============================================================================
# Divide and Conquer
# =============================================================================

def divide_conquer_max_crossing_subarray(my_array, low, mid, high):
    left_sum = float("-inf")
    tmpsum = 0
    for i in range(mid, low-1, -1):
        tmpsum = tmpsum + my_array[i]
        if tmpsum > left_sum:
            left_sum = tmpsum
            max_left = i
    right_sum = float("-inf")
    tmpsum = 0
    for j in range(mid+1, high+1):
        tmpsum = tmpsum + my_array[j]
        if tmpsum > right_sum:
            right_sum = tmpsum
            max_right = j
    return max_left, max_right, left_sum + right_sum
    

def divide_conquer_max_subarray(my_array, low, high):
    # base case
    if high==low:
        return low, high, my_array[low]
    else:
        mid = int((low + high)/2)
        left_low, left_high, left_sum = divide_conquer_max_subarray(my_array, low, mid)
        right_low, right_high, right_sum = divide_conquer_max_subarray(my_array, mid+1, high)
        cross_low, cross_high, cross_sum = divide_conquer_max_crossing_subarray(my_array, low, mid, high)
        if (left_sum >= right_sum) and (left_sum >= cross_sum):
            return left_low, left_high, left_sum
        elif (right_sum >= left_sum) and (right_sum >= cross_sum):
            return right_low, right_high, right_sum
        else:
            return cross_low, cross_high, cross_sum
 
# Generate random array of length between 1 and 10      
x = random.randint(1,10)
my_array = []
for i in range(x):
    my_array.append(random.randint(-100, 100))
 
left, right, maxsum = brute_force_max_subarray(my_array)
print('Brute Force:')  
print('Original subarray: {0}'.format(str(my_array)))
print('Sum of subarray {0} = {1}'.format(str(my_array[left:right]), maxsum))

print('\n')

left, right, maxsum = divide_conquer_max_subarray(my_array, 0, len(my_array)-1)
print('Divide and Conquer:')
print('Original subarray: {0}'.format(str(my_array)))
print('Sum of subarray {0} = {1}'.format(str(my_array[left:right+1]), maxsum))
print('\n')








