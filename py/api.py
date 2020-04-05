#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 13:07:43 2020

@author: root
"""
# =============================================================================
# Package imports
# =============================================================================
import flask
from flask import request, jsonify
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
# Initiali
# =============================================================================
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/optimize', methods=['GET'])
def optimize():
    try:
        # Get args
        schedule_start = request.args.get('schedule_start') # string date %Y-%m-%d
        schedule_end = request.args.get('schedule_end') # string date %Y-%m-%d
        
        min_shift = int(request.args.get('min_shift')) # int betwen 1 and 12
        max_shift = int(request.args.get('max_shift')) # int betwen 1 and 12
        
        print('fucking hello?')
        data = request.get_json()
        
        print(type(min_shift))
        print(type(max_shift))
        open_closed = pd.DataFrame.from_records(data['open_closed']) \
                                  .rename(columns = {'':'Type'}) 
        employee_data = pd.DataFrame.from_records(data['employee_data']) 
        avail_data = pd.DataFrame.from_records(data['avail_data']) 
        labor = pd.DataFrame.from_records(data['labor'])
        print('got arguments')
        # Open and closed hours
        open_closed = open_closed.melt('Type', var_name = 'day_of_week', value_name = 'hour')
        open_closed = open_closed.pivot('day_of_week', 'Type').reset_index(level=0)
        open_closed.columns = open_closed.columns.rename(['drop', 'type']).droplevel('drop')
        open_closed.columns = ['day_of_week', 'close', 'open']
        open_closed['close'] = pd.to_datetime(open_closed['close'].str.upper(), format='%I%p').dt.hour
        open_closed['open'] = pd.to_datetime(open_closed['open'].str.upper(), format='%I%p').dt.hour
        
        print('melted dataframe')
        shifts = generate_shifts(schedule_start, schedule_end, min_shift, max_shift, open_closed)
        print('heyo')
        shifts = optimize_shifts(shifts, labor)
        print('heyo1')
        avail = generate_availability(shifts, avail_data, employee_data)
        print('heyo2')
        results = optimize_assignment(shifts, avail)
        print('heyo3')
        results = format_results(results, employee_data, shifts)
        print('got results')
        return jsonify(results.to_dict('records')), 201
    except Exception as e:
        print(e)
        return jsonify(['failure']), 404

app.run(port=5001)
