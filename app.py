#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 19:46:22 2020

@author: root
"""
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

import pandas as pd

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
                value="tab2",
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
                            end_date=dt(2020, 4, 7).date(),
                            start_date=dt.today().date() + timedelta(7)
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

                        html.Button(id='submit-button', n_clicks=0, children='Optimize me!'),
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
                                multiple=True
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
                                multiple=True
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
                                multiple=True
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


app.layout = html.Div(
    id="big-app-container",
    children=[
        gen_header(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
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

@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return gen_input_tab(), stopped_interval
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


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)