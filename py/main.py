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

os.chdir('/Users/alexlamb/Desktop/Schedule_Opt/py')
from helper import (generate_shifts,
                    generate_availability,
                    gen_labor,
                    optimize_shifts,
                    optimize_assignment,
                    format_results)

# =============================================================================
# Initialized data
# =============================================================================

# Schedule start date and end date
schedule_start = '2020-04-01'
schedule_end = '2020-04-08'

# Min and max shift length
min_shift = 6
max_shift = 9

# Open and closed hours
open_closed = pd.read_csv('../data/open_closed_sample.csv')
open_closed = open_closed.melt('Type', var_name = 'day_of_week', value_name = 'hour')
open_closed = open_closed.pivot('day_of_week', 'Type').reset_index(level=0)
open_closed.columns = open_closed.columns.rename(['drop', 'type']).droplevel('drop')
open_closed.columns = ['day_of_week', 'close', 'open']

# Employee + labor need data
employee_data = pd.read_csv('../data/employees.csv')
avail_data = pd.read_csv('../data/availability.csv')
labor = pd.read_csv('../data/labor_need.csv')

# =============================================================================
# Generate all possible shifts + optimize across labor need
# =============================================================================
shifts = generate_shifts(schedule_start, schedule_end, min_shift, max_shift, open_closed)
shifts = optimize_shifts(shifts, labor)
avail = generate_availability(shifts, avail_data, employee_data)
results = optimize_assignment(shifts, avail)
results = format_results(results, employee_data, shifts)




