import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime
import pandas_datareader.data as web


app = dash.Dash()

df = pd.read_csv('NASDAQcompanylist.csv')
options = []
for position in df.index:
    options.append({'label': '{} {}'.format(position, df.loc[position]['Name']), 'value': df.loc[position]['Symbol']})

app.layout = html.Div([
    html.H1(children='Stock Ticker Dashboard'),
    html.Br(),
    html.Div([
        html.Div([
            html.H3(children='Select Stock Symbol'),
            dcc.Dropdown(options=options,
                         multi=True,
                         value=['ULTI'],
                         id='stock-picker'),
        ],
            style={'padding': 10, 'flex': 1}),
        html.Div([
            html.H3(children='Select start and end Date'),
            dcc.DatePickerRange(id='date-picker',
                                min_date_allowed=datetime(2015, 1, 1),
                                max_date_allowed=datetime.today(),
                                start_date=datetime(2016, 9, 1),
                                end_date=datetime(2018, 9, 1))
        ],
            style={'padding': 10, 'flex': 1}
        ),
        html.Div([
            html.Button('SUBMIT', id='submit')
        ],
            style={'flex': 1}
        )
    ],
        style={'display': 'flex', 'flex-direction': 'row'}
    ),
    html.Br(),
    dcc.Graph(id='lineplot',
              figure={
                  'data': [
                      {'x': [1, 2], 'y':[3, 1]}
                  ]
              }
              ),
])


@app.callback(
    Output('lineplot', 'figure'),
    [Input('submit', 'n_clicks')],
    [State('stock-picker', 'value'),
     State('date-picker', 'start_date'),
     State('date-picker', 'end_date')])
def draw_graph(n_clicks, stocks, start_date, end_date):

    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    for stock in stocks:
        df = web.DataReader(stock, "av-daily", start=start, end=end, api_key='ALPH')
        traces.append({'x': df.index, 'y': df.close, 'name': stock})

    fig = {
        'data': traces,
        'layout': {'title':', '.join(stocks)+' Closing Prices'}
    }
    return fig


if __name__ == '__main__':
    app.run_server()