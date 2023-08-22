import MetaTrader5 as mt5
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output

# display data on the MetaTrader 5 package

print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# establish MetaTrader 5 connection to a specified trading account
if not mt5.initialize(login=62452350, server="Exness-MT5Real8",password="Asdf1234"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

# display data on connection status, server name and trading account
print(mt5.terminal_info())
# display data on MetaTrader 5 version
print(mt5.version())

# Define symbols and timeframes
symbols = ['AUDJPYm', 'AUDUSDm', 'EURUSDm', 'EURCHFm', 'EURAUDm', 'EURJPYm', 'EURGBPm', 'GBPUSDm', 'GBPJPYm', 'XAUUSDm',  'NZDUSDm', 'USDCADm', 'USDCHFm', 'USDJPYm' ]
timeframes = [mt5.TIMEFRAME_D1, mt5.TIMEFRAME_W1, mt5.TIMEFRAME_MN1]

# Get prices data
prices = {}
for symbol in symbols:
    symbol_prices = {}
    for timeframe in timeframes:
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1000)
        rates_frame = pd.DataFrame(rates)
        rates_frame.index = pd.to_datetime(rates_frame['time'], unit='s')
        rates_frame.drop(columns=['time'], inplace=True)
        symbol_prices[timeframe] = rates_frame
    prices[symbol] = symbol_prices

# Identify trends
trend = {}
for symbol in symbols:
    symbol_trend = {}
    for timeframe in timeframes:
        symbol_prices = prices[symbol][timeframe]
        prev_high = symbol_prices['high'].iloc[-2]
        prev_low = symbol_prices['low'].iloc[-2]
        curr_high = symbol_prices['high'].iloc[-1]
        curr_low = symbol_prices['low'].iloc[-1]
        if curr_high > prev_high:
            symbol_trend[timeframe] = 'SELL'
        elif curr_low < prev_low:
            symbol_trend[timeframe] = 'BUY'
        else:
            symbol_trend[timeframe] = 'NO SIGNAL'
    trend[symbol] = symbol_trend

# Create the dashboard
app = dash.Dash(__name__)
server = app.server

# Define the interval (15 menit = 900000 ms)
interval_in_milliseconds = 900000

app.layout = html.Div([
    html.H1("A1 Identification", style={"textAlign": "center"}),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in ['Pair', 'D1', 'W1', 'MN']],
    data=[{'Pair': symbol, 'D1': trend[symbol][mt5.TIMEFRAME_D1], 'W1': trend[symbol][mt5.TIMEFRAME_W1], 'MN': trend[symbol][mt5.TIMEFRAME_MN1]} for symbol in symbols],
    style_table={
            'maxWidth': '850px',  # Set the maximum width of the table
            'margin': 'auto'  # Center-align the table horizontally
    },
    style_cell={
        'textAlign': 'center',
        "font_size": "16px",
        "font_family": "Calibri"
    },
    style_header={
        "backgroundColor": "rgb(230, 230, 230)",
        "fontWeight": "bold"
    },
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
        
            "backgroundColor": "rgb(248, 248, 248)"
            
        },
        {
            "if": {"column_id": "Pair"},
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "D1",
                "filter_query": "{D1} eq 'BUY'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "D1",
                "filter_query": "{D1} eq 'SELL'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "D1",
                "filter_query": "{D1} eq 'NO SIGNAL'"
            },
            "backgroundColor": "grey",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "W1",
                "filter_query": "{W1} eq 'BUY'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "W1",
                "filter_query": "{W1} eq 'SELL'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "W1",
                "filter_query": "{W1} eq 'NO SIGNAL'"
            },
            "backgroundColor": "grey",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "MN",
                "filter_query": "{MN} eq 'BUY'"
            },
            "backgroundColor": "#8CD47E",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "MN",
                "filter_query": "{MN} eq 'SELL'"
            },
            "backgroundColor": "#FF6961",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
        {
            "if": {
                "column_id": "MN",
                "filter_query": "{MN} eq 'NO SIGNAL'"
            },
            "backgroundColor": "grey",
            "color": "black",
            "font_size": "12px",
            "fontWeight": "bold"
        },
    ]
    

),
html.Div(
        children=[
            html.H3("Potensial Setup A1", style={"textAlign": "center"}),
            html.P("Tabel diatas hasil identifikasi setup A1 untuk setiap pasangan mata uang (PAIR) dan timeframe (D1, W1, MN1) menggunakan SOP Trading A1."),
            html.P("")
        ],
        style={"textAlign": "center", "marginTop": "18px"}
    ),
    # Add the dcc.Interval component to the layout
    dcc.Interval(
        id='interval-component',
        interval=interval_in_milliseconds,  # in milliseconds
        n_intervals=0
    )
])

# Define the callback to update the data table at the specified interval
@app.callback(
    Output('table', 'data'),
    [Input('interval-component', 'n_intervals')]
)
def update_table_data(n):
    # The code to update the data here
    # For example, you can rerun the data retrieval and processing code here
    # For simplicity, let's just reuse the existing data for now
    data = [{'Pair': symbol, 'D1': trend[symbol][mt5.TIMEFRAME_D1], 'W1': trend[symbol][mt5.TIMEFRAME_W1], 'MN': trend[symbol][mt5.TIMEFRAME_MN1]} for symbol in symbols]
    return data


if __name__ == '__main__':
    app.run_server(debug=True)