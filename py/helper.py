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
    shift_avail = shift_avail[['employee_name', 'index']]
    shift_avail = pd.DataFrame(shift_avail.groupby('employee_name')['index'].apply(lambda x: list(x)))
    shift_avail = shift_avail.merge(employee_data, how = 'left', on = 'employee_name').set_index('employee_name')
    
    return shift_avail.to_dict(orient = 'index')

def generate_hours(start, end):
    # Create all hours between these two dates
    date_hour_range = pd.date_range(start=start, end=end, freq='H')[:-1]
    
    df = pd.DataFrame([date_hour_range , 
                          date_hour_range.day_name(), 
                          date_hour_range.hour]).T.reset_index()
    df.columns = ['timeslot', 'datetime', 'day_of_week', 'hour']
    return df

def generate_availability_old(df_hours, df_employee, df_avail):
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
                  on = 'employee_name').drop(['employee_email'], axis = 1)
    df.set_index(['timeslot', 'employee_name'], inplace = True)
    return df

def generate_hourly_need(df_hours, df_labor):
    df = df_hours.merge(df_labor,
                        how = 'left',
                        on = ['day_of_week', 'hour'])
    df.drop(['day_of_week', 'hour'], axis = 1, inplace = True)
    return df
        
