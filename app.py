#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 19:46:22 2020

@author: root
"""

# =============================================================================
# Package imports
# =============================================================================
from datetime import datetime as dt
from datetime import timedelta
import os
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import dash_table
import requests 
import io
import json
import pandas as pd
import base64

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config["suppress_callback_exceptions"] = True

dows = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
initial_hours = [['Open', '12am', '12am', '12am', '12am', '12am', '12am', '12am'], ['Close', '12pm', '12pm', '12pm', '12pm', '12pm', '12pm', '12pm']]
initial_hours = pd.DataFrame(initial_hours, columns = dows)

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# =============================================================================
# Layout generators
# =============================================================================
def gen_header():
    return html.Div(
        id="header",
        className="header",
        children=[
            html.Div(
                id="header-text",
                children=[
                    html.H5("Schedule Optimization Software"),
                    html.H6("Input your employee information and get an optimized schedule!"),
                ],
            ),
            html.Div(
                id="header-logo",
                children=[
                    html.Img(id="logo", src=app.get_asset_url("panda.png")),
                ],
            ),
        ],
    )


def gen_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="input-tab",
                        label="Schedule inputs",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="output-tab",
                        label="Schedule outputs",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

def gen_input_tab():
    return [
        # Manually select metrics
        html.Div(
            id="set-input-intro-container",
            # className='twelve columns',
            children=[
                html.Div(
                    id='inputs',
                    children = [
                        html.Br(),
                        html.P("What dates do you want a schedule for?"),
                        dcc.DatePickerRange(
                            id='schedule-date-range',
                            min_date_allowed=dt(1995, 8, 5),
                            max_date_allowed=dt(2030, 9, 19),
                            initial_visible_month=dt(2020, 4, 1),
                            end_date=dt.today().date() + timedelta(7),
                            start_date=dt.today().date()
                        ),
                        html.Br(),
                        html.Br(),
                        html.P("How many hours can shifts be?"),
                        dcc.RangeSlider(
                            id='shift-lengths',
                            marks={i: '{}'.format(i) for i in range(1, 13)},
                            min=1,
                            max=12,
                            value=[6,8]
                        ),
                        html.Br(),
                        html.P('Fill in your open hours below'),
                        dash_table.DataTable(
                            id='hours-table',
                            columns=[{"name": i, "id": i} for i in initial_hours.columns],
                            data=initial_hours.to_dict('records'),
                            editable=True,
                            style_header={'backgroundColor': '#1e2130'},
                            style_cell={
                                'backgroundColor': '#1e2130',
                                'color': 'white'
                            },
                        ),
                        html.Br(),
                        html.Button('Optimize me!', id='submit-button'),
                        html.Div(
                            id='button-output',
                            children = [
                                html.P('')
                        ]),
                    ]),
                    html.Div(
                        id='uploads',
                        children = [
                            html.Br(),
                            html.P('Upload your employee information below'),
                            dcc.Upload(
                                id='upload-info',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=False
                            ),
                            html.Br(),
                            html.P('Upload your employee availability below'),
                            dcc.Upload(
                                id='upload-availability',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=False
                            ),
                            html.Br(), 
                            html.P('Upload your labor need below'),
                            dcc.Upload(
                                id='upload-labor-need',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=False
                            ),
                        ]),

        ]),
    ]

def gen_output_tab():
    return [
        html.Div(
            id="set-output-intro-container",
            children=[
                html.P( "Am here.  Hi.  Tab 2."),
            ]
        )]

# =============================================================================
# App layout
# =============================================================================

app.layout = html.Div(
    id="big-app-container",
    children=[
        gen_header(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,
            n_intervals=50,  
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                gen_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="n-interval-stage", data=50),
    ],
)

# =============================================================================
# Render callbacks
# =============================================================================

@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return gen_input_tab(), stopped_interval
    if tab_switch == "tab2":
        return gen_output_tab(), stopped_interval

@app.callback(
    Output("n-interval-stage", "data"),
    [Input("app-tabs", "value")],
    [
        State("interval-component", "n_intervals"),
        State("interval-component", "disabled"),
        State("n-interval-stage", "data"),
    ],
)
def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
    if disabled:
        return cur_interval

    if tab_switch == "tab1":
        return cur_interval
    return cur_stage

# =============================================================================
# Submit optimization callbacks
# =============================================================================
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))

    return df.to_dict('records')


@app.callback(
    [Output("button-output", "children")],
    [Input("submit-button", "n_clicks")],
    [State("schedule-date-range", "start_date"),
      State("schedule-date-range", "end_date"),
      State("shift-lengths", "value"),
      State("hours-table", "data"),
      State("upload-info", "contents"),
      State("upload-info", "filename"),
      State("upload-availability", "contents"),
      State("upload-availability", "filename"),
      State("upload-labor-need", "contents"),
      State("upload-labor-need", "filename"),],
)
def submit(n_clicks, start_date, end_date, shift_lengths, open_hours, 
           emp_info, emp_name, availability, avail_name, labor_need, labor_name):
    print('in submit')
    if n_clicks > 0:

        emp_info = parse_contents(emp_info, emp_name)
        availability = parse_contents(availability, avail_name)
        labor_need = parse_contents(labor_need, labor_name)


        # params & url 
        URL = "http://127.0.0.1:5001/optimize"
        HEADERS = {'Content-Type': 'application/json'}
        PARAMS = {'schedule_start': start_date,
                  'schedule_end': end_date,
                  'min_shift': shift_lengths[0],
                  'max_shift': shift_lengths[1]
        } 
          
        json_data = {'employee_data': emp_info,
                'avail_data': availability,
                'labor': labor_need,
                'open_closed': open_hours
        }
        
        print(PARAMS)
        
        print(json_data)
        # sending get request and saving the response as response object 
        r = requests.get(url = URL, 
                         headers = HEADERS, 
                         params = PARAMS, 
                         json = json_data) 
          
        # extracting data in json format 
        print(r.status_code)
        if r.status_code == 201:
            return [html.P('Optimization submitted')]
        else:
            return [html.P(str(r.content))]
    else:
        return []
    
# Running the server
if __name__ == "__main__":
    app.run_server(threaded=True, debug=True, port=8050)