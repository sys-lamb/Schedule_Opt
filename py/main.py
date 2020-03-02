#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 15:59:34 2020

@author: alexlamb
"""
# =============================================================================
# Package imports + directory changes
# =============================================================================

import os
import pandas as pd
import numpy as np
import pandas as pd
import pulp
os.chdir('/Users/alexlamb/Desktop/Schedule_Opt/py')
from helper import (generate_hours, 
                    generate_availability,
                    generate_hourly_need)

# =============================================================================
# Main run
# =============================================================================

# Schedule start date and end date
schedule_start = '2020-04-01'
schedule_end = '2020-04-08'
# Employee + labor need data
employee_data = pd.read_csv('../data/employees.csv')
availability_data = pd.read_csv('../data/availability.csv')
laborhour_data = pd.read_csv('../data/labor_need.csv')

hours = generate_hours(schedule_start, schedule_end)
hours_avail = generate_availability(hours, employee_data, availability_data)
labor_need = generate_hourly_need(hours, laborhour_data)
hour_limits = hours_avail.reset_index()[['employee_name', 'min_hours', 'max_hours']].drop_duplicates().set_index('employee_name')

timeslots = labor_need['timeslot']
employees = hours_avail.index.levels[1]

# =============================================================================
# Set up optimization problem
# =============================================================================
prob = pulp.LpProblem('GenSchedule', pulp.LpMinimize) # Minimize costs

scheduled = pulp.LpVariable.dicts('scheduled',
                                ((timeslot, employee_name) for timeslot, employee_name in hours_avail.index),
                                 lowBound=0,
                                 cat='Binary')

# Minimization function                           
prob += pulp.lpSum(
    [scheduled[timeslot, employee_name] * hours_avail.loc[(timeslot, employee_name), 'hourly_rate'] 
    for timeslot, employee_name in hours_avail.index]
)

# Balance labor need with staffing
for timeslot in timeslots:
    prob += (sum([scheduled[(timeslot, employee)] for employee in employees]) 
    == labor_need.loc[timeslot, 'labor_need'])

# Check availability
for timeslot in timeslots:
    for employee in employees:
        if hours_avail.loc[(timeslot, employee), 'avail'] == 0:
            prob += scheduled[timeslot, employee] == 0

# Check min hours
for employee in employees:
    prob += (sum([scheduled[(timeslot, employee)] for timeslot in timeslots])
    >= hour_limits.loc[employee, 'min_hours']) 
    
# Check max hours
for employee in employees:
    prob += (sum([scheduled[(timeslot, employee)] for timeslot in timeslots])
    <= hour_limits.loc[employee, 'max_hours']) 

prob.solve()
print(pulp.LpStatus[prob.status])

output = []
for timeslot, employee in scheduled:
    var_output = {
        'Timeslot': timeslot,
        'Employee': employee,
        'Scheduled': scheduled[(timeslot, employee)].varValue,
    }
    output.append(var_output)
output_df = pd.DataFrame.from_records(output)#.sort_values(['timeslot', 'staffmember'])
output_df.set_index(['Timeslot', 'Employee'], inplace=True)
if pulp.LpStatus[prob.status] == 'Optimal':
    print(output_df)









