#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:41:15 2020

@author: alexlamb
"""

import pandas as pd
import numpy as np

# =============================================================================
# Helper functions
# =============================================================================
def generate_hours(start, end):
    # Create all hours between these two dates
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
                  on = 'employee_name').drop(['employee_email'], axis = 1)
    df.set_index(['timeslot', 'employee_name'], inplace = True)
    return df

def generate_hourly_need(df_hours, df_labor):
    df = df_hours.merge(df_labor,
                        how = 'left',
                        on = ['day_of_week', 'hour'])
    df.drop(['day_of_week', 'hour'], axis = 1, inplace = True)
    return df
        
