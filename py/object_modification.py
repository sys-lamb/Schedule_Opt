#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import itertools
from scipy.optimize import minimize
import os
os.chdir('/Users/alexlamb/Desktop/Schedule_Opt/py')

def min_func(x, shift_lengths, shift_starts, labor_req, labor_req_starts):
    
    # Determine which labor req entries are covered by which shifts for constraints
    shifts_in_labor_req = []
    for i in range(len(labor_req)):
        shifts_in = []
        for j in range(len(shift_lengths)):
            if((shift_starts[j] <= labor_req_starts[i]) & ((shift_starts[j] + shift_lengths[j]) > labor_req_starts[i])):
                shifts_in.append(j)
        shifts_in_labor_req.append(shifts_in)

    diffs = []
    for i in range(len(labor_req)):
        shift_req = 0
        for j in shifts_in_labor_req[i]:
            shift_req = shift_req + x[j]
        diffs.append(shift_req/labor_req[i])
        
    return np.mean(diffs)
        
def build_constraints(shift_lengths, shift_starts, labor_req, labor_req_starts):   

    # Determine which labor req entries are covered by which shifts for constraints
    shifts_in_labor_req = []
    for i in range(len(labor_req)):
        shifts_in = []
        for j in range(len(shift_lengths)):
            if((shift_starts[j] <= labor_req_starts[i]) & ((shift_starts[j] + shift_lengths[j]) > labor_req_starts[i])):
                shifts_in.append(j)
        shifts_in_labor_req.append(shifts_in)
    
    # Dynamically build constraints
    constraints = []
    for i in range(len(labor_req)):
        if (len(shifts_in_labor_req[i]) > 0):
            constraint =  'lambda x: ' + str(-1 * labor_req[i])
            for j in shifts_in_labor_req[i]:
                constraint = constraint + ' + x[' + str(j) + '] '
            constraints.append(constraint)
    
    cons = ()
    for eq in constraints:
        cons = cons + ({'type': 'ineq', 'fun': eval(eq)},)
    
    for i in range(len(shift_starts)):
        con = 'lambda x: x[' + str(i) + ']'
        cons = cons + ({'type': 'ineq', 'fun': eval(con)},)

    return cons


def gen_labor(shift_starts,  shift_lengths, labor_req, labor_req_starts):

    cons = build_constraints(shift_lengths, shift_starts, labor_req, labor_req_starts)
    x = [np.mean(labor_req)] * len(shift_lengths)
    res = minimize(min_func, x, args = (shift_lengths, shift_starts, labor_req, labor_req_starts), constraints=cons, method='SLSQP', options={'disp': False})
    labor = np.array(np.round(res.x))

    return labor

def gen_shift_labor(shifts_, labor_):
    
    shift_days = list(set(shifts_.day_of_week.unique()))
    daily_shifts = []
    for day in shift_days:
        tmp = shifts_[shifts_['day_of_week'] == day]
        tmp1 = labor_[labor_['day_of_week'] == day]

        shift_starts = list(tmp['start_hour'])
        shift_lengths = list(tmp['end_hour'] - tmp['start_hour'])
        
        labor_req = list(tmp1['labor_need'])
        labor_req_starts = list(tmp1['hour'])
        
        if((len(labor_req) > 0) & (sum(np.round(labor_req)) > 0)):
            labor = gen_labor(shift_starts, shift_lengths, labor_req, labor_req_starts)
            tmp['req'] = labor
            daily_shifts.append([tmp['index'], tmp['req']])
    
    return daily_shifts
            
