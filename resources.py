import dash
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

base_url = 'https://api1.binance.com'

connectivity = '/api/v3/ping'
kilnes = '/api/v3/klines'

key = os.environ['API_KEY']

price_generator = None
current_window = None
trade_table = None
balance = 100
columns = ['Action', 'Time', 'Price', 'Quantity', 'Cash Balance']
long_ma_trend = []
short_ma_trend = []
current_trend = []
time = []
fees = 0.001

long_period = 10
short_period = 5