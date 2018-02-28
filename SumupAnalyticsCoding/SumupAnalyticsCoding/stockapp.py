import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import *
import colorlover as cl
from flask_cors import CORS
import pandas as pd
import numpy as np
import quandl

app = dash.Dash()
server = app.server
CORS(server)

quandl.ApiConfig.api_key = '<insert the key>'
app.scripts.config.serve_locally = False
colorscale = cl.scales['9']['qual']['Paired']


# Read the List of Tickers for EOD
df_symbol = pd.read_csv('ticker_list.csv')



#JS and CSS Defenitons
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-latest.min.js'
external_css = ["https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

#App Layout
app.layout = html.Div([
    html.Div([
        html.H2('Stock Displaying App')
    ]),
    dcc.Dropdown(
        id='ticker-input',
        options=[{'label': s[0], 'value': s[1]}
                 for s in zip(df_symbol.Name, df_symbol.Ticker,df_symbol.Exchange)],
        value=['AAPL'],
        multi=True
    ),
    html.Div(id='graphs')
], className="container")


# Moving average Function
def moving_average(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

# Defenitions for Updating graphs in the Layout.
@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('ticker-input', 'value')])
def update_graph(tickers):
    graphs = []
    for i, ticker in enumerate(tickers):
        try:
            tickid="EOD/"+ticker
            df = quandl.get(tickid)
        except:
            graphs.append(html.H3(
                'Data is not available for {}'.format(ticker),
                style={'marginTop': 20, 'marginBottom': 20}
            ))
            continue
        x = df.index
        y = df.Close
        ma = moving_average(y, 10)
        xy_data = Scatter(x=x, y=y, mode='markers', marker=Marker(size=2), name=ticker)
        mov_avg = Scatter(x=x, y=ma, line=Line(width=2, color='red'), name='Moving average')
        #data = Data([xy_data, mov_avg])
        graphs.append(dcc.Graph(
            id=ticker,
            figure={
                'data':[xy_data, mov_avg],
                'layout': {
                    'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                    'legend': {'x': 0}
                }
            }
        ))
    return graphs


if __name__ == '__main__':
    app.run_server(port=7777)