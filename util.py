from dash.dependencies import Input, Output, State
from resources import app, base_url, connectivity, key, kilnes, data_1000_min
import requests
import dash
import plotly.express as px
import pandas as pd

@app.callback(
    Output(component_id='api-response', component_property='children'),
    Input(component_id='test-api', component_property='n_clicks'),
    State(component_id='api-response', component_property='children')
)
def test_api(n_clicks, prev):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    response = requests.get(base_url + connectivity, headers={'X-MBX-APIKEY': key})
    return str(response.headers._store)

@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    Input(component_id='1000-min', component_property='n_clicks')
)
def last_1000_min(n_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    response = requests.get(base_url + kilnes,
                            params={'symbol': 'ADABTC', 'interval': '1m', 'limit': 1000},
                            headers={'X-MBX-APIKEY': key})

    df = pd.DataFrame({
        "Time (min)": [i for i in range(len(response.json()))],
        "Open": [float(item[1])*100/float(response.json()[0][1]) - 100 for item in response.json()],
        "High": [float(item[2])*100/float(response.json()[0][2]) - 100 for item in response.json()],
        "Low": [float(item[3]) * 100 / float(response.json()[0][3]) - 100 for item in response.json()]
    })

    fig = px.line(df.melt(id_vars="Time (min)"), x='Time (min)', y='value', color='variable')
    return fig