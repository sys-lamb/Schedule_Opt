#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:41:15 2020

@author: alexlamb
"""

import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
from scipy.optimize import minimize
import pulp as pl
import collections as cl

# =============================================================================
# Helper functions
# =============================================================================
def generate_shifts(schedule_start, schedule_end, min_shift, max_shift, open_closed):
    
    d1 = dt.strptime(schedule_start, '%Y-%m-%d')
    d2 = dt.strptime(schedule_end, '%Y-%m-%d')
    hours = pd.date_range(d1, d2, freq='H')
    shifts = [[x, x + timedelta(hours = y)] for x in hours for y in range(min_shift, max_shift + 1)]
    shifts = pd.DataFrame(shifts, columns = ['start','end'])
    shifts['day_of_week'] = shifts['start'].dt.day_name()
    shifts['start_hour'] = shifts['start'].dt.hour
    shifts['end_hour'] = shifts['end'].dt.hour
    
    shifts = shifts.merge(open_closed, how = 'outer', on = 'day_of_week')
    shifts['interday'] = np.where(shifts['start'].dt.date == shifts['end'].dt.date, 0, 1)
    shifts['is_open'] = ((shifts['interday'] == 0) & (shifts['end_hour'] < shifts['close']) & (shifts['start_hour'] >= shifts['open']))
    shifts = shifts[shifts['is_open'] == True]
    
    shifts.drop(['close', 'open', 'interday', 'is_open'], axis = 1, inplace = True)
    shifts.reset_index(inplace = True)

    return shifts

def generate_availability(shifts, avail_data, employee_data):
    
    shift_avail = avail_data.merge(shifts, how = 'outer', on = 'day_of_week')

    shift_avail['is_avail'] = ((shift_avail['start_hour'] >= shift_avail['start_avail_time']) & 
                               (shift_avail['end_hour'] < shift_avail['end_avail_time']))
    
    shift_avail = shift_avail[shift_avail['is_avail'] == True]
    shift_avail['duration'] = shift_avail['end_hour'] - shift_avail['start_hour']
    shift_avail = shift_avail[['employee_name', 'pos_index', 'duration']]
    shift_avail = pd.DataFrame(shift_avail.groupby('employee_name').agg({'pos_index': lambda x: list(x),
                                                                         'duration': lambda x: list(x)}))
    shift_avail = shift_avail.merge(employee_data, how = 'left', on = 'employee_name').set_index('employee_name')
    
    return shift_avail.to_dict(orient = 'index')

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

def optimize_shifts(shifts_, labor_):
    
    shift_starts = list(shifts_['start_hour'])
    shift_lengths = list(shifts_['end_hour'] - shifts_['start_hour'])
    
    labor_req = list(labor_['labor_need'])
    labor_req_starts = list(labor_['hour'])
            
    shift_days = list(set(shifts_.day_of_week.unique()))
    daily_shifts = pd.DataFrame()
    for day in shift_days:
        tmp = shifts_[shifts_['day_of_week'] == day]
        tmp1 = labor_[labor_['day_of_week'] == day]
    
        shift_starts = list(tmp['start_hour'])
        shift_lengths = list(tmp['end_hour'] - tmp['start_hour'])
        
        labor_req = list(tmp1['labor_need'])
        labor_req_starts = list(tmp1['hour'])
        
        if((len(labor_req) > 0) & (sum(np.round(labor_req)) > 0)):
            reqs = gen_labor(shift_starts, shift_lengths, labor_req, labor_req_starts)
            tmp['req'] = reqs
            daily_shifts = pd.concat([daily_shifts, tmp[['index', 'req']]], axis = 0)
    
    shifts_ = shifts_.merge(daily_shifts, how = 'left', on = 'index')
    shifts_ = shifts_[shifts_['req'] > 0].reset_index() \
                                      .drop('level_0', axis = 1) \
                                      .reset_index() \
                                      .rename(columns = {'level_0':'pos_index'}) 
    
    return shifts_

def optimize_assignment(shifts_, avail_):
    
    shift_reqs = list(shifts_['req'])
    
    prob = pl.LpProblem("roster", pl.LpMinimize)

    cost = []
    vars_by_shift = cl.defaultdict(list)
    vars_by_worker = cl.defaultdict(list) #max shifts
    
    for worker, info in avail_.items():
        for shift in info['pos_index']:
            worker_var = pl.LpVariable("%s_%s" % (worker, shift), 0, 1, pl.LpInteger)
            vars_by_shift[shift].append(worker_var)
            cost.append(worker_var * (info['hourly_rate']* info['duration']))
    
    prob += sum(cost)
    
    for shift, requirement in enumerate(shift_reqs):
        prob += sum(vars_by_shift[shift]) >= requirement
    
    status = prob.solve()
    print("Result:", pl.LpStatus[status])
    results = []
    for shift, vars in vars_by_shift.items():
        results.append({
            "shift": shift,
            "workers": [var.name for var in vars if var.varValue == 1],
        })

    return results

def format_results(results_, employee_data, shifts):
    results_ = pd.DataFrame(results_)
    lst_col = 'workers'
    results_ = pd.DataFrame({
          col:np.repeat(results_[col].values, results_[lst_col].str.len())
          for col in results_.columns.drop(lst_col)}
        ).assign(**{lst_col:np.concatenate(results_[lst_col].values)})[results_.columns]
    
    results_['workers'] = results_['workers'].apply(lambda x: x.split('_')[0])
    results_ = results_.merge(employee_data, how = 'left', left_on = 'workers', right_on = 'employee_name')
    results_ = results_.merge(shifts, how = 'left', left_on = 'shift', right_on = 'pos_index')
    results_['duration'] = results_['end_hour'] - results_['start_hour']
    results_['shift_cost'] = results_['duration'] * results_['hourly_rate']
    
    return results_
    
        
        
    
    
    
    
    
