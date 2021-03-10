import dash
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

base_url = 'https://api1.binance.com'

connectivity = '/api/v3/ping'

key = os.environ['API_KEY']