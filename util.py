from dash.dependencies import Input, Output, State
from resources import app, base_url, connectivity, key
import requests

@app.callback(
    Output(component_id='api-response', component_property='children'),
    Input(component_id='test-api', component_property='n_clicks'),
    State(component_id='api-response', component_property='children')
)
def test_api(n_clicks, prev):
    response = requests.get(base_url + connectivity, headers={'X-MBX-APIKEY': key})
    return str(response.headers._store)