import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# import user files
import Graphs as graphs

labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
values = [4500,2500,1053,500]

trace = go.Pie(labels=labels, values=values)

iplot([trace])

Stocks = pd.read_csv('Data\Stocks\S&P 500 (^GSPC)_2005to2018_daily.csv')
Stocks['Date'] = pd.to_datetime(Stocks.Date, infer_datetime_format=True)

app = dash.Dash(__name__)
# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

app.layout = html.Div([
            html.Div([
            html.H1("Stock VS Happiness",
                style={'textAlign': 'center',
                   'fontSize': 40,
                   'marginTop': 25,
                   'marginBottom': 0
    }),
    html.H2("Agenda: Explore relationship between stock & happiness",
            style={'textAlign': 'center',
                   'fontSize': 25,
                   'marginTop':0,
                   'marginBottom': 20
    }),
],className='row'),

    html.Div([
        html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'High', 'value': 'High'},
            {'label': 'Low', 'value': 'Low'},
        ],
        multi=True,
        value=['High'],
        style={
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            "width": "50%",
        }
    ),
    dcc.Graph(id='my-graph')
], className='six columns')
]),
])

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    dropdown = {
        "High": "High",
        "Low": "Low",
    }
    high = []
    low = []

    for i in selected_dropdown_value:
        if i=="High":
            data = 'High'
            high.append(go.Scatter(
x=Stocks["Date"],
                y=Stocks[data],
                mode='lines',
                opacity=0.7,
                name=f'{dropdown[i]} Price',
                textposition='bottom center',

        ))
        else:
            low.append(go.Scatter(
                x=Stocks["Date"],
                y=Stocks["Low"],
                mode='lines',
                opacity=0.6,
                name=f'{dropdown[i]} Price',
                textposition='bottom center',
             ))

    traces = [high, low]
    data = [val for sublist in traces for val in sublist]
    figure = {
        'data': data,
        'layout': go.Layout(
            colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
            height=400,
            width=600,
            title=f"Stock prices for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
            xaxis={"title":"Date",
                'rangeselector': {'buttons': list([
                {'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                {'step': 'all'}
            ])}, 'rangeslider': {'visible': True}, 'type': 'date'},
            yaxis={
                "title":"Stock Prices (USD)",
            }
        )

    }
    return figure


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
