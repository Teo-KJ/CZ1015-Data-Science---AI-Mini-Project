import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output


Stocks = pd.read_csv('Data\Stocks\S&P 500 (^GSPC)_2005to2018_daily.csv')
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Emissions%20Data.csv')
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
                   'marginBottom': 0,
                    'font-family':'algerian'
    }),
    html.H3("Agenda: Explore relationship between stock & happiness",
            style={'textAlign': 'center',
                   'fontSize': 25,
                   'marginTop':0,
                   'marginBottom': 20,
                   'font-family':'algerian'
    }),
],className='row'),

    html.Div([
        html.Div([
            html.H5("Stock Price over time",
            style={'textAlign':'center',
                'font-family':'algerian'
            }),
        ],className='six columns'),

        html.Div([
        html.H5("Greenhouse Gas Emissions by Continent",
            style={"textAlign": "center",
                'font-family':'algerian',
                'margin-left':'45%'
            }),
    ],className='six columns'),
],className='row'),

    html.Div([
        html.Div([
        dcc.Dropdown(
        id='stock-dropdown',
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
], className='six columns'),

    html.Div([
        dcc.RangeSlider(
            id="select-year",
            min=2008,
            max=2011,
            marks={2008: "2008", 2009: "2009", 2010: "2010", 2011: "2011"},
            value=[2008, 2010],

        )], className='six columns',
            style={
        "display": "block",
        "margin-left": "65%",
        "width": "35%",
    }
    ),
],className='row'),

    html.Div([
        html.Div([
    dcc.Graph(id='stocktime')
    ],className='six columns'),
        html.Div([
    dcc.Graph(id="stockboxplot")
    ],className='six columns'),
        ],className='row'),
    ],className='ten columns offset-by-one')

@app.callback(Output('stocktime', 'figure'),
              [Input('stock-dropdown', 'value')])

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

@app.callback(
    Output('stockboxplot', 'figure'),
    [Input('select-year', 'value')])
def update_figure(selected):
    dff = df[(df["Year"] >= selected[0]) & (df["Year"] <= selected[1])]
    traces = []
    for continent in dff.Continent.unique():
        traces.append(go.Box(
            y=dff[dff["Continent"] == continent]["Emission"],
            name=continent,
            marker={"size": 4}

        ))

    return {

        "data": traces,
        "layout": go.Layout(
            title=f"Emission Levels for {'-'.join(str(i) for i in selected)}",
            height=400,
            width=600,
            xaxis={
                "showticklabels": False,
            },
            yaxis={
                "title": f"Emissions (gigatonnes of CO2)",
                "type": "log",
            },

        )

    }

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
