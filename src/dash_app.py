import dash 
from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px

from datetime import datetime
## ====================================================
import pandas as pd

## ====================================================
# local imports
from src.raystate_class import RayState
from src.raytracer.raytracer import RayTracer
from src.bindings.coordinates_class import LLA
from src.bindings.timeandlocation_class import TimeAndLocation
## ====================================================
app = dash.Dash(__name__)

# initial structure
heights_m = [0, 100, 1000, 10000, 100000, 1000000]
indexN =    [1.0, 1.0, 0.95, 0.95, 0.97, 1.0]
params = ['Exit Elevation', 'Exit Azimuth', 'Latitude', 'Longitude', 'Altitude', 'n']
columnsNames = [{'id': p, 'name': p} for p in params]

## ===================================================
## Layout

app.layout = html.Div([
    html.Div(children=[

        html.H4(children='Initial Path Entry'),
        html.Div(dcc.Input(id='input_elevation', type='number', placeholder = "Initial Elevation Angle [deg]")),
        html.Div(dcc.Input(id='input_azimuth', type='number', placeholder = "Initial Azimuth Angle [deg]")),
        html.Div(dcc.Input(id='input_n', type='number', placeholder = "Initial Index of Refraction")),
        html.Div(dcc.Input(id='input_latitude', type='number', placeholder = "Initial Latitude [deg]")),
        html.Div(dcc.Input(id='input_longitude', type='number', placeholder = "Initial Longitude [deg]")),
        html.Div(dcc.Input(id='input_altitude', type='number', placeholder = "Initial Altitude [m]")),

        html.Button('Run Ray Tracer', id='execute_ray', n_clicks=0),

        dash_table.DataTable(
            id='table_editing',
            columns = columnsNames,
            data=[],
            editable=True
    ),
    ], style={'padding': 10, 'flex': 1}),

    html.Div(children=[

        html.H4(children='Lat/Lon Path'),
        dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='crossfilter-yaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            ),
        dcc.Graph(
                id='longitude_chart', figure = {}
            ),
        dcc.Graph(
                id='latitude_chart', figure = {}
            ),

    ], style={'padding': 10, 'flex': 1}), 
    dcc.Store(id='session', storage_type='session'),
], style={'display': 'flex', 'flex-direction': 'row'})

## ===================================================
## Callback & Callback action
# add a click to the appropriate store.
@app.callback(
    Output('session', 'data'),
    [Input('execute_ray', 'n_clicks')], 
    [State(component_id ='input_elevation', component_property='value'), 
        State(component_id ='input_azimuth', component_property='value'),
        State(component_id ='input_n', component_property='value'),
        State(component_id ='input_latitude', component_property='value'),
        State(component_id ='input_longitude', component_property='value'),
        State(component_id ='input_altitude', component_property='value')])
def on_click(n_clicks, input_elevation, input_azimuth, input_n, input_latitude, input_longitude, input_altitude):
    initialLLA = LLA(input_latitude, input_longitude, input_altitude)
    initialState = RayState(exitElevation_deg=input_elevation,exitAzimuth_deg= input_azimuth, 
        lla=initialLLA, nIndex=input_n)
    if n_clicks == 0:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate
    else:
        if(initialState.isNone()):
            raise PreventUpdate
        else:
            print("Running Ray Tracer")
            eventTimeAndLocation = TimeAndLocation(eventLocation_LLA=initialLLA, eventTime_UTC=datetime.now)
            rayTracer = RayTracer(timeAndLocation=eventTimeAndLocation)
            rayStates = rayTracer.execute(heights_m = heights_m, indexN = indexN, params=[input_azimuth, input_elevation])
            listTmp = []
            columnNames = []
            for rayState in rayStates:
                tmpList = rayState.generateList()
                listTmp.append(tmpList)
                columnNames = rayState.generateColumnNames()

            df = pd.DataFrame(listTmp, columns = columnNames, dtype = float)
            return df.to_dict()

## ===================================================
## Callback & Callback action
@app.callback(
    [Output('table_editing', 'data'), Output('table_editing', 'columns')],
    Input('session', 'modified_timestamp'),
    State('session', 'data')
)   
def on_click(ts, data):
    if ts == -1:
        raise PreventUpdate
    df = pd.DataFrame(data)
    columns = [{'id': p, 'name': p} for p in df.columns]
    data = df.to_dict(orient = 'records')
    return data, columns

## ===================================================
## Callback & Callback action
@app.callback(
    Output('longitude_chart', 'figure'),
    Input('session', 'modified_timestamp'),
    [State('session', 'data'), State('crossfilter-yaxis-type', 'value')]
)
def on_click(ts, data, yaxis_type):
    if ts == -1:
        raise PreventUpdate
    df = pd.DataFrame(data)
    fig = px.scatter(x=df['Longitude'],  y=df['Altitude'],
        hover_name=df['Exit Azimuth'])
    fig.update_yaxes(title='Altitude [m]', type='linear' if yaxis_type == 'Linear' else 'log')
    fig.update_xaxes(title='Longitude [deg]', type='linear')

    return(fig) 
   
## ===================================================
## Callback & Callback action
@app.callback(
    Output('latitude_chart', 'figure'),
    Input('session', 'modified_timestamp'),
    [State('session', 'data'), State('crossfilter-yaxis-type', 'value')]
)
def on_click(ts, data, yaxis_type):
    if ts == -1:
        raise PreventUpdate
    df = pd.DataFrame(data)
    fig = px.scatter(x=df['Latitude'],  y=df['Altitude'],
        hover_name=df['Exit Elevation'])
    fig.update_yaxes(title='Altitude [m]', type='linear' if yaxis_type == 'Linear' else 'log')
    fig.update_xaxes(title='Latitude [deg]', type='linear')
    return(fig)   

if __name__ == '__main__':
    app.run_server(debug=True)