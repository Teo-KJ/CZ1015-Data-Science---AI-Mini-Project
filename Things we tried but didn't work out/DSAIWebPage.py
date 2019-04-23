import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import flask
import glob
import os
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Stocks Datasets
Stocks = pd.read_csv('Data\Stocks\S&P 500 (^GSPC)_2005to2018_daily.csv')
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Emissions%20Data.csv')
Stocks['Date'] = pd.to_datetime(Stocks.Date, infer_datetime_format=True)

China_Stocks = pd.read_csv('Data\Stocks\SSE Composite Index (^SSEC)_2006to2017_daily.csv')
China_Stocks = China_Stocks.dropna()
# PRC_Resulting_Stocks_Data = stocks_data_2(China_Stocks)

# Import the WHR Dataset
d1 = pd.read_excel("Data/World Happiness Report/WHR2019.xlsx", sheet_name='Table2.1')
US_Data =  pd.DataFrame(d1[(d1['Country name'] == "United States")])
US_Data_LL = list(US_Data['Life Ladder'])

# Others
image_directory = '/Users/tkjie/Desktop/'
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
static_image_route = '/static/'

app = dash.Dash(__name__)
app.title = 'Cx1015 Mini Project'

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
    
    html.Div(children='''
        Over here, we examine the relationship of the stocks and happiness over the course of the period where World Happiness
        Index had been measured.
    ''', style={'fontSize':20, 'textAlign': 'center'}),

    html.Div(html.Img(src = 'https://geology.com/world/world-map.gif',
            style = {'height':'15%', 'width':'30%', 'position':'relative', 'margin-top':20, 'margin-left':'35%'})), html.Br(),

    html.Div([
        dcc.Dropdown(
        id='image-dropdown',
        options=[{'label': i[:-4], 'value': i} for i in list_of_images],
        value=list_of_images[0], style={'margin-left':'20%', 'width':550}#,'padding': 10}
    ), html.Br(),
    html.Img(id='image', style={'margin-left':"40%"})]),

    html.Div([
        html.Div([
            html.H5("Stock Price Over Time",
            style={'textAlign':'center', 'fontSize': 25,
                'font-family':'algerian',
                'marginRight':'15%'
            }),
        ],className='six columns'),

        html.Div([
        html.H5("Greenhouse Gas Emissions by Continent",
            style={"textAlign": "right","fontSize":25,
                'font-family':'algerian',
                'margin-right':'20%'
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
            "margin-right": "15%",
            "width": "70%",
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
        "margin-left": "60%",
        "width": "35%",
    }
    ),
],className='row'),
    
    html.Div([
        html.Div([
    dcc.Graph(id='stocktime')
    ],className='six columns',
    style={'margin-left':'0%'}),


    html.Div([
    dcc.Graph(id="Greenhouseboxplot")
    ],className='six columns'),
        ],className='row'),

  
    ],className='ten columns offset-by-one')

@app.callback(Output('stocktime', 'figure'),
              [Input('stock-dropdown', 'value')])

def update_graph_US(selected_dropdown_value):
    dropdown = {
        "High": "High",
        "Low": "Low",}
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
                line=dict(color='#5E0DAC')
        ))
        else:
            low.append(go.Scatter(
                x=Stocks["Date"],
                y=Stocks["Low"],
                mode='lines',
                opacity=0.6,
                name=f'{dropdown[i]} Price',
                textposition='bottom center',
                line=dict(color='#FF4F00')
             ))

    traces = [high, low]
    data = [val for sublist in traces for val in sublist]
    figure = {
        'data': data,
        'layout': go.Layout(
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
    Output('Greenhouseboxplot', 'figure'),
    [Input('select-year', 'value')])

def update_figure(selected):
    dff = df[(df["Year"] >= selected[0]) & (df["Year"] <= selected[1])]
    traces = []
    for continent in dff.Continent.unique():
        traces.append(go.Box(
            y=dff[dff["Continent"] == continent]["Emission"],
            name=continent,
            marker={"size": 4}))
    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Emission Levels for {'-'.join(str(i) for i in selected)}",
            height=400,
            width=600,
            xaxis={
                "showticklabels": False,
            },
            yaxis={"title": f"Emissions (gigatonnes of CO2)","type": "log",},
        )
    }

@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('image-dropdown', 'value')])

def update_image_src(value):
    return static_image_route + value

# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
