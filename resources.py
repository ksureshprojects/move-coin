import dash
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

base_url = 'https://api1.binance.com'

connectivity = '/api/v3/ping'
kilnes = '/api/v3/klines'

key = os.environ['API_KEY']

data_1000_min = []