from dash.dependencies import Input, Output, State
from resources import app, base_url, connectivity, key, kilnes, \
    price_generator, current_window, long_period, short_period, trade_table, \
    balance, fees, columns, long_ma_trend, short_ma_trend, current_trend, time
import requests
import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


@app.callback(
    Output(component_id='api-response', component_property='children'),
    Input(component_id='test-api', component_property='n_clicks')
)
def test_api(n_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    response = requests.get(base_url + connectivity, headers={'X-MBX-APIKEY': key})
    return str(response.headers._store)


@app.callback(Output(component_id='ma-crossover-graph', component_property='figure'),
              Output(component_id='trade-table', component_property='columns'),
              Output(component_id='trade-table', component_property='data'),
              Input(component_id='interval-component', component_property='n_intervals')
              # Input(component_id='next-interval', component_property='n_clicks')
              )
def run_ma_crossover(n_intervals):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    if n_intervals == 1:
        long_ma_trend.clear()
        short_ma_trend.clear()
        current_trend.clear()
        time.clear()

        long_ma, short_ma, current, low, high = get_next_price(first=True)
        global trade_table
        trade_table = pd.DataFrame(columns=columns)
        update_trade_table(long_ma, short_ma, n_intervals, low, high)

        long_ma_trend.append(long_ma)
        short_ma_trend.append(short_ma)
        current_trend.append(current)
        time.append(n_intervals)

    else:
        long_ma, short_ma, current, low, high = get_next_price()

        update_trade_table(long_ma, short_ma, n_intervals, low, high)

        long_ma_trend.append(long_ma)
        short_ma_trend.append(short_ma)
        current_trend.append(current)
        time.append(n_intervals)

    fig = go.Figure(layout=go.Layout(
        xaxis=go.layout.XAxis(title="Minute"),
        yaxis=go.layout.YAxis(title="Price")
    ))
    fig.add_trace(go.Scatter(x=time, y=long_ma_trend, mode="lines", name="Long MA"))
    fig.add_trace(go.Scatter(x=time, y=short_ma_trend, mode="lines", name="Short MA"))
    fig.add_trace(go.Scatter(x=time, y=current_trend, mode="lines", name="Current"))

    return fig, [{"name": i, "id": i} for i in trade_table.columns], trade_table.to_dict('records')


def get_next_price(first=False):
    if first:
        response = requests.get(base_url + kilnes,
                                params={'symbol': 'ADABTC', 'interval': '1m', 'limit': 1000},
                                headers={'X-MBX-APIKEY': key})
        global price_generator
        price_generator = iter(response.json())
        global current_window
        # col_ind: 1 - Open, 2 - High, 3 - Low
        current_window = np.array([next(price_generator) for _ in range(long_period)]).astype(float)
        return calculate_values(current_window)
    else:
        current_window = np.vstack((current_window[1:, :], np.array(next(price_generator)))).astype(float)
        return calculate_values(current_window)


def calculate_values(window):
    long_ma = np.average(window[:, 1])
    short_ma = np.average(window[long_period - short_period:, 1])
    current = window[-1, 1]
    high = window[-1, 2]
    low = window[-1, 3]
    return long_ma, short_ma, current, high, low


def update_trade_table(long_ma, short_ma, n_intervals, low, high):
    global balance, trade_table
    values = trade_table.values.tolist()
    if short_ma >= long_ma and (len(values) == 0 or values[-1][0] == 'SELL'):
        quantity = (balance - balance * fees)/high
        balance = 0
        values.append(['BUY', n_intervals, high, quantity, balance])
        trade_table = pd.DataFrame(values, columns=columns)
    elif long_ma >= short_ma and len(values) > 0 and values[-1][0] == 'BUY':
        quantity = values[-1][3]
        balance = (quantity - quantity * fees) * low
        values.append(['SELL', n_intervals, low, quantity, balance])
        trade_table = pd.DataFrame(values, columns=columns)


@app.callback(Output(component_id='interval-component', component_property='disabled'),
              Output(component_id='interval-component', component_property='n_intervals'),
              Input(component_id='ma-crossover', component_property='n_clicks'))
def start_ma_crossover(n_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    if n_clicks % 2 == 0:
        return True, 0
    else:
        return False, 0


@app.callback(Output(component_id='1000-min-graph', component_property='figure'),
              Input(component_id='1000-min', component_property='n_clicks'))
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

