#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 15:59:34 2020

@author: alexlamb
"""

# Import packages and directories
import os
import pandas as pd
import mip
import numpy as np
os.chdir('/Users/alexlamb/Desktop/Schedule_Opt/py')
from classes import Employee, LaborHour, Shift

# Read in data (to be inputted by user)
employee_data = pd.read_csv('../data/employees.csv', engine='python')
availability_data = pd.read_csv('../data/availability.csv')
laborhour_data = pd.read_csv('../data/labor_need.csv')

min_hours = 6
max_hours = 10

# Create Employee objects from inputted data
employees = []
for idx, row in employee_data.iterrows():
    emp = Employee(row['employee_name'], row['employee_email'], row['hourly_rate'])
    employees.append(emp)   

# Create LaborHour objects from inputted data
laborhours = []
for idx, row in laborhour_data.iterrows():
    hour = LaborHour(row['day_of_week'], row['hour'], row['labor_need'])
    laborhours.append(hour)   

# Optimize + create Shifts from Laborhours


















