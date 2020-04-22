#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:50:17 2020

@author: root
"""

import pandas as pd
import numpy as np
import json 
import ast



labor_need = '''[{'day_of_week': 'Monday', 'labor_need': 2, 'hour': 8}, {'day_of_week': 'Monday', 'labor_need': 2, 'hour': 9}, {'day_of_week': 'Monday', 'labor_need': 3, 'hour': 10}, {'day_of_week': 'Monday', 'labor_need': 3, 'hour': 11}, {'day_of_week': 'Monday', 'labor_need': 3, 'hour': 12}, {'day_of_week': 'Monday', 'labor_need': 3, 'hour': 13}, {'day_of_week': 'Monday', 'labor_need': 4, 'hour': 14}, {'day_of_week': 'Monday', 'labor_need': 4, 'hour': 15}, {'day_of_week': 'Monday', 'labor_need': 2, 'hour': 16}, {'day_of_week': 'Monday', 'labor_need': 2, 'hour': 17}, {'day_of_week': 'Monday', 'labor_need': 1, 'hour': 18}, {'day_of_week': 'Monday', 'labor_need': 1, 'hour': 19}, {'day_of_week': 'Monday', 'labor_need': 1, 'hour': 20}, {'day_of_week': 'Tuesday', 'labor_need': 2, 'hour': 8}, {'day_of_week': 'Tuesday', 'labor_need': 2, 'hour': 9}, {'day_of_week': 'Tuesday', 'labor_need': 3, 'hour': 10}, {'day_of_week': 'Tuesday', 'labor_need': 3, 'hour': 11}, {'day_of_week': 'Tuesday', 'labor_need': 3, 'hour': 12}, {'day_of_week': 'Tuesday', 'labor_need': 3, 'hour': 13}, {'day_of_week': 'Tuesday', 'labor_need': 4, 'hour': 14}, {'day_of_week': 'Tuesday', 'labor_need': 4, 'hour': 15}, {'day_of_week': 'Tuesday', 'labor_need': 2, 'hour': 16}, {'day_of_week': 'Tuesday', 'labor_need': 2, 'hour': 17}, {'day_of_week': 'Tuesday', 'labor_need': 1, 'hour': 18}, {'day_of_week': 'Tuesday', 'labor_need': 1, 'hour': 19}, {'day_of_week': 'Tuesday', 'labor_need': 1, 'hour': 20}, {'day_of_week': 'Wednesday', 'labor_need': 2, 'hour': 8}, {'day_of_week': 'Wednesday', 'labor_need': 2, 'hour': 9}, {'day_of_week': 'Wednesday', 'labor_need': 3, 'hour': 10}, {'day_of_week': 'Wednesday', 'labor_need': 3, 'hour': 11}, {'day_of_week': 'Wednesday', 'labor_need': 3, 'hour': 12}, {'day_of_week': 'Wednesday', 'labor_need': 3, 'hour': 13}, {'day_of_week': 'Wednesday', 'labor_need': 4, 'hour': 14}, {'day_of_week': 'Wednesday', 'labor_need': 4, 'hour': 15}, {'day_of_week': 'Wednesday', 'labor_need': 2, 'hour': 16}, {'day_of_week': 'Wednesday', 'labor_need': 2, 'hour': 17}, {'day_of_week': 'Wednesday', 'labor_need': 1, 'hour': 18}, {'day_of_week': 'Wednesday', 'labor_need': 1, 'hour': 19}, {'day_of_week': 'Wednesday', 'labor_need': 1, 'hour': 20}, {'day_of_week': 'Thursday', 'labor_need': 2, 'hour': 8}, {'day_of_week': 'Thursday', 'labor_need': 2, 'hour': 9}, {'day_of_week': 'Thursday', 'labor_need': 3, 'hour': 10}, {'day_of_week': 'Thursday', 'labor_need': 3, 'hour': 11}, {'day_of_week': 'Thursday', 'labor_need': 3, 'hour': 12}, {'day_of_week': 'Thursday', 'labor_need': 3, 'hour': 13}, {'day_of_week': 'Thursday', 'labor_need': 4, 'hour': 14}, {'day_of_week': 'Thursday', 'labor_need': 4, 'hour': 15}, {'day_of_week': 'Thursday', 'labor_need': 2, 'hour': 16}, {'day_of_week': 'Thursday', 'labor_need': 2, 'hour': 17}, {'day_of_week': 'Thursday', 'labor_need': 1, 'hour': 18}, {'day_of_week': 'Thursday', 'labor_need': 1, 'hour': 19}, {'day_of_week': 'Thursday', 'labor_need': 1, 'hour': 20}, {'day_of_week': 'Friday', 'labor_need': 2, 'hour': 8}, {'day_of_week': 'Friday', 'labor_need': 2, 'hour': 9}, {'day_of_week': 'Friday', 'labor_need': 3, 'hour': 10}, {'day_of_week': 'Friday', 'labor_need': 3, 'hour': 11}, {'day_of_week': 'Friday', 'labor_need': 3, 'hour': 12}, {'day_of_week': 'Friday', 'labor_need': 3, 'hour': 13}, {'day_of_week': 'Friday', 'labor_need': 4, 'hour': 14}, {'day_of_week': 'Friday', 'labor_need': 4, 'hour': 15}, {'day_of_week': 'Friday', 'labor_need': 2, 'hour': 16}, {'day_of_week': 'Friday', 'labor_need': 2, 'hour': 17}, {'day_of_week': 'Friday', 'labor_need': 1, 'hour': 18}, {'day_of_week': 'Friday', 'labor_need': 1, 'hour': 19}, {'day_of_week': 'Friday', 'labor_need': 1, 'hour': 20}, {'day_of_week': 'Saturday', 'labor_need': 2, 'hour': 8}, {'day_of_week': 'Saturday', 'labor_need': 2, 'hour': 9}, {'day_of_week': 'Saturday', 'labor_need': 3, 'hour': 10}, {'day_of_week': 'Saturday', 'labor_need': 3, 'hour': 11}, {'day_of_week': 'Saturday', 'labor_need': 3, 'hour': 12}, {'day_of_week': 'Saturday', 'labor_need': 3, 'hour': 13}, {'day_of_week': 'Saturday', 'labor_need': 4, 'hour': 14}, {'day_of_week': 'Saturday', 'labor_need': 4, 'hour': 15}, {'day_of_week': 'Saturday', 'labor_need': 2, 'hour': 16}, {'day_of_week': 'Saturday', 'labor_need': 2, 'hour': 17}, {'day_of_week': 'Saturday', 'labor_need': 1, 'hour': 18}, {'day_of_week': 'Saturday', 'labor_need': 1, 'hour': 19}, {'day_of_week': 'Saturday', 'labor_need': 1, 'hour': 20}, {'day_of_week': 'Sunday', 'labor_need': 2, 'hour': 8}, {'day_of_week': 'Sunday', 'labor_need': 2, 'hour': 9}, {'day_of_week': 'Sunday', 'labor_need': 3, 'hour': 10}, {'day_of_week': 'Sunday', 'labor_need': 3, 'hour': 11}, {'day_of_week': 'Sunday', 'labor_need': 3, 'hour': 12}, {'day_of_week': 'Sunday', 'labor_need': 3, 'hour': 13}, {'day_of_week': 'Sunday', 'labor_need': 4, 'hour': 14}, {'day_of_week': 'Sunday', 'labor_need': 4, 'hour': 15}, {'day_of_week': 'Sunday', 'labor_need': 2, 'hour': 16}, {'day_of_week': 'Sunday', 'labor_need': 2, 'hour': 17}, {'day_of_week': 'Sunday', 'labor_need': 1, 'hour': 18}, {'day_of_week': 'Sunday', 'labor_need': 1, 'hour': 19}, {'day_of_week': 'Sunday', 'labor_need': 1, 'hour': 20}]'''

labor_need = ast.literal_eval(labor_need)
labor_need = pd.DataFrame.from_records(labor_need)



test = {"shifts":[{"shift": 9, "workers": "c", "employee_name": "c", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 9, "index": 245, "start": "2020-04-20 08:00:00", "end": "2020-04-20 16:00:00", "day_of_week": "Monday", "start_hour": 8, "end_hour": 16, "req": 2.0, "duration": 8, "shift_cost": 96}, {"shift": 9, "workers": "d", "employee_name": "d", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 9, "index": 245, "start": "2020-04-20 08:00:00", "end": "2020-04-20 16:00:00", "day_of_week": "Monday", "start_hour": 8, "end_hour": 16, "req": 2.0, "duration": 8, "shift_cost": 96}, {"shift": 10, "workers": "d", "employee_name": "d", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 10, "index": 251, "start": "2020-04-20 10:00:00", "end": "2020-04-20 18:00:00", "day_of_week": "Monday", "start_hour": 10, "end_hour": 18, "req": 1.0, "duration": 8, "shift_cost": 96}, {"shift": 11, "workers": "c", "employee_name": "c", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 11, "index": 258, "start": "2020-04-20 13:00:00", "end": "2020-04-20 19:00:00", "day_of_week": "Monday", "start_hour": 13, "end_hour": 19, "req": 1.0, "duration": 6, "shift_cost": 72}, {"shift": 12, "workers": "c", "employee_name": "c", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 12, "index": 317, "start": "2020-04-21 08:00:00", "end": "2020-04-21 16:00:00", "day_of_week": "Tuesday", "start_hour": 8, "end_hour": 16, "req": 2.0, "duration": 8, "shift_cost": 96}, {"shift": 12, "workers": "d", "employee_name": "d", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 12, "index": 317, "start": "2020-04-21 08:00:00", "end": "2020-04-21 16:00:00", "day_of_week": "Tuesday", "start_hour": 8, "end_hour": 16, "req": 2.0, "duration": 8, "shift_cost": 96}, {"shift": 13, "workers": "b", "employee_name": "b", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 10, "min_hours": 32, "max_hours": 60, "pos_index": 13, "index": 323, "start": "2020-04-21 10:00:00", "end": "2020-04-21 18:00:00", "day_of_week": "Tuesday", "start_hour": 10, "end_hour": 18, "req": 1.0, "duration": 8, "shift_cost": 80}, {"shift": 14, "workers": "c", "employee_name": "c", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 14, "index": 330, "start": "2020-04-21 13:00:00", "end": "2020-04-21 19:00:00", "day_of_week": "Tuesday", "start_hour": 13, "end_hour": 19, "req": 1.0, "duration": 6, "shift_cost": 72}, {"shift": 16, "workers": "c", "employee_name": "c", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 16, "index": 395, "start": "2020-04-22 10:00:00", "end": "2020-04-22 18:00:00", "day_of_week": "Wednesday", "start_hour": 10, "end_hour": 18, "req": 1.0, "duration": 8, "shift_cost": 96}, {"shift": 17, "workers": "c", "employee_name": "c", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 17, "index": 402, "start": "2020-04-22 13:00:00", "end": "2020-04-22 19:00:00", "day_of_week": "Wednesday", "start_hour": 13, "end_hour": 19, "req": 1.0, "duration": 6, "shift_cost": 72}, {"shift": 19, "workers": "d", "employee_name": "d", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 19, "index": 467, "start": "2020-04-23 10:00:00", "end": "2020-04-23 18:00:00", "day_of_week": "Thursday", "start_hour": 10, "end_hour": 18, "req": 1.0, "duration": 8, "shift_cost": 96}, {"shift": 20, "workers": "a", "employee_name": "a", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 10, "min_hours": 32, "max_hours": 60, "pos_index": 20, "index": 474, "start": "2020-04-23 13:00:00", "end": "2020-04-23 19:00:00", "day_of_week": "Thursday", "start_hour": 13, "end_hour": 19, "req": 1.0, "duration": 6, "shift_cost": 60}, {"shift": 0, "workers": "a", "employee_name": "a", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 10, "min_hours": 32, "max_hours": 60, "pos_index": 0, "index": 26, "start": "2020-04-17 08:00:00", "end": "2020-04-17 16:00:00", "day_of_week": "Friday", "start_hour": 8, "end_hour": 16, "req": 2.0, "duration": 8, "shift_cost": 80}, {"shift": 0, "workers": "d", "employee_name": "d", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 0, "index": 26, "start": "2020-04-17 08:00:00", "end": "2020-04-17 16:00:00", "day_of_week": "Friday", "start_hour": 8, "end_hour": 16, "req": 2.0, "duration": 8, "shift_cost": 96}, {"shift": 1, "workers": "a", "employee_name": "a", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 10, "min_hours": 32, "max_hours": 60, "pos_index": 1, "index": 32, "start": "2020-04-17 10:00:00", "end": "2020-04-17 18:00:00", "day_of_week": "Friday", "start_hour": 10, "end_hour": 18, "req": 1.0, "duration": 8, "shift_cost": 80}, {"shift": 2, "workers": "d", "employee_name": "d", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 2, "index": 39, "start": "2020-04-17 13:00:00", "end": "2020-04-17 19:00:00", "day_of_week": "Friday", "start_hour": 13, "end_hour": 19, "req": 1.0, "duration": 6, "shift_cost": 72}, {"shift": 3, "workers": "a", "employee_name": "a", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 10, "min_hours": 32, "max_hours": 60, "pos_index": 3, "index": 101, "start": "2020-04-18 08:00:00", "end": "2020-04-18 16:00:00", "day_of_week": "Saturday", "start_hour": 8, "end_hour": 16, "req": 2.0, "duration": 8, "shift_cost": 80}, {"shift": 3, "workers": "b", "employee_name": "b", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 10, "min_hours": 32, "max_hours": 60, "pos_index": 3, "index": 101, "start": "2020-04-18 08:00:00", "end": "2020-04-18 16:00:00", "day_of_week": "Saturday", "start_hour": 8, "end_hour": 16, "req": 2.0, "duration": 8, "shift_cost": 80}, {"shift": 4, "workers": "c", "employee_name": "c", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 4, "index": 107, "start": "2020-04-18 10:00:00", "end": "2020-04-18 18:00:00", "day_of_week": "Saturday", "start_hour": 10, "end_hour": 18, "req": 1.0, "duration": 8, "shift_cost": 96}, {"shift": 5, "workers": "d", "employee_name": "d", "employee_email": "cs3337.001@gmail.com", "hourly_rate": 12, "min_hours": 32, "max_hours": 60, "pos_index": 5, "index": 114, "start": "2020-04-18 13:00:00", "end": "2020-04-18 19:00:00", "day_of_week": "Saturday", "start_hour": 13, "end_hour": 19, "req": 1.0, "duration": 6, "shift_cost": 72}]
}

df1 = pd.DataFrame.from_records(test['shifts'])
df = df1.groupby(['shift', 'req', 'day_of_week', 'start_hour', 'end_hour'])['employee_name'].nunique().reset_index()
df['key'] = 1
index = pd.DataFrame(list(range(1,25)), columns = ['hour'])
index['key'] = 1
df = df.merge(index, how = 'left', on = 'key' )
df = df[(df['hour'] < df['end_hour']) & (df['hour'] >= df['start_hour'])]
df = df.drop(['key', 'start_hour', 'end_hour'], axis = 1)
df = df.merge(df1[['shift', 'start']], how = 'left', on = 'shift')
df['start'] = df['start'].apply(lambda x: x[0:10]) 
df['start'] = df['start'] + ' ' + df['hour'].astype(str) + ':00'


