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
        
        min_shift = request.args.get('min_shift')# int betwen 1 and 12
        max_shift = request.args.get('max_shift') # int betwen 1 and 12
        
        data = request.get_json()
        
        print(min_shift)
        print(max_shift)
        print(data)
        open_closed = data['open_closed'] # csv
        employee_data = data['employee_data'] # csv
        avail_data = data['avail_data'] # csv
        labor = data['labor'] # csv
    
        # Open and closed hours
        open_closed = open_closed.melt('Type', var_name = 'day_of_week', value_name = 'hour')
        open_closed = open_closed.pivot('day_of_week', 'Type').reset_index(level=0)
        open_closed.columns = open_closed.columns.rename(['drop', 'type']).droplevel('drop')
        open_closed.columns = ['day_of_week', 'close', 'open']
    
        shifts = generate_shifts(schedule_start, schedule_end, min_shift, max_shift, open_closed)
        shifts = optimize_shifts(shifts, labor)
        avail = generate_availability(shifts, avail_data, employee_data)
        results = optimize_assignment(shifts, avail)
        results = format_results(results, employee_data, shifts)
    
        return jsonify(results), 201
    except:
        return [], 404

app.run(port=5001)
