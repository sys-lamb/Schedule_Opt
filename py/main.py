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

# =============================================================================
# Helper functions
# =============================================================================
def generate_hours(start, end):
    # Create all hours between these two dates
    date_range = pd.date_range(start=start, end=end)
    date_hour_range = pd.date_range(start=start, end=end, freq='H')[:-1]
    
    df = pd.DataFrame([date_hour_range , 
                          date_hour_range.day_name(), 
                          date_hour_range.hour]).T.reset_index()
    df.columns = ['timeslot', 'datetime', 'day_of_week', 'hour']
    return df

def generate_availability(df_hours, df_employee, df_avail):
    # Find all datetimes that an employee is available
    df = df_hours.merge(df_avail, 
                        how = 'outer', 
                        on = 'day_of_week')
  
    df['avail'] = np.where((df['start_avail_time'] <= df['hour']) 
                            & (df['end_avail_time'] >= df['hour']), 
                            1, 0)
    df.drop(['start_avail_time', 'end_avail_time', 'day_of_week', 'datetime', 'hour'], axis = 1, inplace = True)
    df = df.merge(df_employee,
                  how = 'left',
                  on = 'employee_name').drop(['employee_email', 'min_hours'], axis = 1)
    df.set_index(['timeslot', 'employee_name'], inplace = True)
    return df

def generate_hourly_need(df_hours, df_labor):
    df = df_hours.merge(df_labor,
                        how = 'outer',
                        on = ['day_of_week', 'hour'])
    df.drop(['timeslot', 'day_of_week', 'hour'], axis = 1, inplace = True)
    return df

# =============================================================================
# Main run
# =============================================================================

# Schedule start date and end date
schedule_start = '2020-04-01'
schedule_end = '2020-04-07'
# Employee + labor need data
employee_data = pd.read_csv('../data/employees.csv')
availability_data = pd.read_csv('../data/availability.csv')
laborhour_data = pd.read_csv('../data/labor_need.csv')

hours = generate_hours(schedule_start, schedule_end)
hours_avail = generate_availability(hours, employee_data, availability_data)
labor_need = generate_hourly_need(hours, laborhour_data)

staffed = pulp.LpVariable.dicts("scheduled",
                                ((timeslot, employee) for timeslot, employee
                                 in hours_avail.index),
                                 lowBound=0,
                                 cat='Binary')














