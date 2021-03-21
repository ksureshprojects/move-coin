# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_core_components as dcc
import dash_html_components as html
import dash_table
from resources import app
from util import test_api, last_1000_min

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Button(
        id='test-api',
        children='Test API'
    ),

    html.Div(
        id='api-response',
        children=''
    ),

    html.Button(
        id='1000-min',
        children='1000 min'
    ),

    dcc.Graph(
        id='1000-min-graph'
        # figure=fig
    ),

    html.Button(
        id='ma-crossover',
        children='Start MA Crossover'
    ),

    html.Button(
        id='next-interval',
        children='Next Interval'
    ),

    dcc.Interval(
        id='interval-component',
        interval=1000, # in milliseconds
        n_intervals=0,
        disabled=True
    ),

    dcc.Graph(
        id='ma-crossover-graph'
        # figure=fig
    ),

    dash_table.DataTable(
        id='trade-table'
        # columns=[{"name": i, "id": i} for i in df.columns],
        # data=df.to_dict('records'),
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)