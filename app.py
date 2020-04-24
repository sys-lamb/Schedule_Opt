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
import dash_bootstrap_components as dbc
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import requests 
import io
import json
import pandas as pd
import base64
import smtplib, ssl
from email.message import EmailMessage
import re

# Initialize dash app
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config["suppress_callback_exceptions"] = True
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# Initialize some data for the app to display
dows = ['', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
initial_hours = [['Open', '12am', '12am', '12am', '12am', '12am', '12am', '12am'], ['Close', '12pm', '12pm', '12pm', '12pm', '12pm', '12pm', '12pm']]
initial_hours = pd.DataFrame(initial_hours, columns = dows)

# Helper function to compare labor need to scheduled staffing
def gen_comparison(df1):
    
    data = json.loads(df1)
    df1= pd.DataFrame.from_records(data)  

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
    df = df[['start', 'req', 'employee_name']].drop_duplicates().sort_values('start')

    return df

# Generate total cost of the schedule
def gen_total_cost(df1):
    
    data = json.loads(df1)
    df= pd.DataFrame.from_records(data)  

    df['shift_cost'] = df['hourly_rate'] * df['duration']
    total_cost = df['shift_cost'].sum()
    return 'Schedule cost: $' + str(total_cost)

# Generate labor hour overage/underage
def gen_overage(df1):
    
    data = json.loads(df1)
    df1= pd.DataFrame.from_records(data)  

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
    df = df[['start', 'req', 'employee_name']].drop_duplicates().sort_values('start')
    
    overage = df['req'].sum() - df['employee_name'].sum()
    if overage > 0:
        overage = str(round(overage)) + ' labor hours short' 
    elif overage == 0:
        overage = 'Labor requirements exactly staffed'
    else:
        overage = str(round(overage)) + ' labor hours over' 
        
    return overage

# =============================================================================
# Layout generators
# =============================================================================

# HTML layout for page header
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
            html.Div(id="tab-container",
            className="tabs",
            children = [
                dbc.Tabs(
                    [
                        dbc.Tab(label="Optimizer Input", 
                                tab_id="tab1", 
                                tab_style={"margin-left": "auto"},
                                className="custom-tabs"),
                        dbc.Tab(label="Schedule Output", 
                                tab_id="tab2", 
                                label_style={"color": "#00AEF9"},
                                className="custom-tabs"),
                    ],
                    id="tabs",
                    card=True,
                    active_tab="tab1",
                ),
                
            ]),
            html.Div(
                id="header-logo",
                children=[
                    html.Img(id="logo", src=app.get_asset_url("panda.png")),
                ],
            ),
        ],
    )


# HTML layout for two tab links
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

# HTML layout for input tab
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

# HTML layout for output tab
def gen_output_tab(df, overage, total_cost):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x = list(df['start'].values),
        y = list(df['req'].values),
        name = 'Labor Requirement'
    ))
    
    fig.add_trace(go.Scatter(
        x = list(df['start'].values),
        y = list(df['employee_name'].values),
        name = 'Employees Staffed'
    ))
    
    fig.update_layout(
        title = "Labor Requirements x Optimized Staffing",
        yaxis = dict(
          scaleanchor = "x",
          scaleratio = 1,
          rangemode='tozero'
        )
    )
        
    return [
        html.Div(
            id="set-output-intro-container",
            children=[
                html.Div(id='outer-output-div',
                    children = [
                        html.Div(
                        id='email-outputs',
                        children = [
                            dcc.Input(id="email", type="text", placeholder="Email"),
                            html.P('  '),
                            dcc.Input(id="password", type="password", placeholder="Password"),
                            html.P('  '),
                            html.Button('Email schedules!', id='email-button'),
                            html.Br(),
                            html.Div(id="email-output", children=['']),

                        ]),
                        html.Div(
                            id='metrics-text',
                            children = [
                                html.P(total_cost),
                                html.P(overage),
                        ]),
                        html.Div(
                            id='metrics-output',
                            children = [html.Div([
                                    dcc.Graph(
                                    id='example-graph',
                                        figure=fig
                                    )
                                ])
                        ]),  

                ]),
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

                html.Div(id="content"),
                # Main app
            ],
        ),
        html.Div(
            id='optimization-output',
            children = [
                html.P('')
            ], style={'display': 'none'}
        ),

        dcc.Store(id="n-interval-stage", data=50),
    ],
)

# =============================================================================
# Render callbacks
# =============================================================================

@app.callback(Output("content", "children"), 
              [Input("tabs", "active_tab")],
              [State("optimization-output", "children")])
def switch_tab(at, data):
    if at == "tab1":
        return gen_input_tab()
    elif at == "tab2":
        print('tab2')
        df = gen_comparison(data)
        overage = gen_overage(data)
        total_cost = gen_total_cost(data)
        return gen_output_tab(df, overage, total_cost)
    return html.P("This shouldn't ever be displayed...")

# =============================================================================
# User action callbacks
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

# Send user inputs to the api and return optimized output   
@app.callback(
    [Output("optimization-output", "children")],
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

        # sending get request and saving the response as response object 
        r = requests.get(url = URL, 
                         headers = HEADERS, 
                         params = PARAMS, 
                         json = json_data) 
          
        # extracting data in json format 
        print(r.status_code)
        if r.status_code == 201:
            encoding = 'utf-8'
            return [r.content.decode(encoding)]
        else:
            print(r.content)
            return ['']
    else:
        return []
   
# Send email to each of the employees with their schedule
@app.callback(
    [Output("email-output", "children")],
    [Input("email-button", "n_clicks")],
    [State("optimization-output", "children"),
     State("email", "value"),
     State("password", "value")]
)
def send_email(n_clicks, data, sender_email, password):
    print('in submit')
    if n_clicks > 0:
        data = json.loads(data)
        data = pd.DataFrame.from_records(data)    
        
        port = 587  # For starttls
        smtp_server = "smtp.gmail.COM"
     
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.connect('smtp.gmail.com', '587')
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
        
            for x in data.employee_name.unique():
                tmp = data.query("employee_name == '{0}'".format(x))
                receiver_name = tmp.employee_name.unique()[0]
                receiver_email = tmp.employee_email.unique()[0]
                
                print(receiver_name)
                # Create the container email message.
                msg = EmailMessage()
                msg['Subject'] = 'Upcoming Schedule'
                msg['From'] = sender_email
                msg['To'] = receiver_email
                message = """\
                Hi there, {0}
                You are scheduled for the following shifts:       
                """.format(receiver_name)
                message = re.sub('    ','',message)
                for idx, row in tmp.iterrows():
                    shift_row = '{0} {1} from {2} to {3}\n'.format(row['day_of_week'], 
                                                                   row['start'][0:10],
                                                                   row['start_hour'], 
                                                                   row['end_hour'])
                    message = message + shift_row
    
                msg.set_content(message)
                server.send_message(msg)
    return ['Emails sent!']

# Running the app on the server
if __name__ == "__main__":
    app.run_server(threaded=True, debug=True, port=8050)