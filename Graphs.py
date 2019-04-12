import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sb
import math
# import matplotlib.pyplot as plt
# import plotly.plotly as py
# import plotly.graph_objs as go
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot,iplot
# init_notebook_mode(connected=True)
import os
from statsmodels.tsa.holtwinters import ExponentialSmoothing, Holt

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Global variables 
some_range = range(len(y_train)+50,len(y_train)+50+len(predictions))



def stocks_data_1(data):
    data["Log10_volume"] = np.log10(data['Volume'])
    data["Average"] = (data["High"] + data["Low"])/2
    data["Perc Diff"] = ((data['High']-data['Low'])/data['High'])*100
    data["Delta"] = ((data['High']-data['Low']))
    
    Stocks_2006 = pd.DataFrame(data[data['Date'].str.contains('/2006')])
    Stocks_2007 = pd.DataFrame(data[data['Date'].str.contains('/2007')])
    Stocks_2008 = pd.DataFrame(data[data['Date'].str.contains('/2008')])
    Stocks_2009 = pd.DataFrame(data[data['Date'].str.contains('/2009')])
    Stocks_2010 = pd.DataFrame(data[data['Date'].str.contains('/2010')])
    Stocks_2011 = pd.DataFrame(data[data['Date'].str.contains('/2011')])
    Stocks_2012 = pd.DataFrame(data[data['Date'].str.contains('/2012')])
    Stocks_2013 = pd.DataFrame(data[data['Date'].str.contains('/2013')])
    Stocks_2014 = pd.DataFrame(data[data['Date'].str.contains('/2014')])
    Stocks_2015 = pd.DataFrame(data[data['Date'].str.contains('/2015')])
    Stocks_2016 = pd.DataFrame(data[data['Date'].str.contains('/2016')])
    Stocks_2017 = pd.DataFrame(data[data['Date'].str.contains('/2017')])
    Stocks_2018 = pd.DataFrame(data[data['Date'].str.contains('/2018')])
    
    frames = [Stocks_2006, Stocks_2007, Stocks_2008, Stocks_2009, Stocks_2010, Stocks_2011, Stocks_2012, Stocks_2013,
              Stocks_2014, Stocks_2015, Stocks_2016, Stocks_2017, Stocks_2018]
    
    Resulting_Data = pd.concat(frames)
    print("Total number of days:", len(Resulting_Data))
    return Resulting_Data

def stocks_data_2(data):
    data["Log10_volume"] = np.log10(data['Volume'])
    data["Average"] = (data["High"] + data["Low"])/2
    data["Perc Diff"] = ((data['High']-data['Low'])/data['High'])*100
    data["Delta"] = ((data['High']-data['Low']))
    
    Stocks_2006 = pd.DataFrame(data[data['Date'].str.contains('2006-')])
    Stocks_2007 = pd.DataFrame(data[data['Date'].str.contains('2007-')])
    Stocks_2008 = pd.DataFrame(data[data['Date'].str.contains('2008-')])
    Stocks_2009 = pd.DataFrame(data[data['Date'].str.contains('2009-')])
    Stocks_2010 = pd.DataFrame(data[data['Date'].str.contains('2010-')])
    Stocks_2011 = pd.DataFrame(data[data['Date'].str.contains('2011-')])
    Stocks_2012 = pd.DataFrame(data[data['Date'].str.contains('2012-')])
    Stocks_2013 = pd.DataFrame(data[data['Date'].str.contains('2013-')])
    Stocks_2014 = pd.DataFrame(data[data['Date'].str.contains('2014-')])
    Stocks_2015 = pd.DataFrame(data[data['Date'].str.contains('2015-')])
    Stocks_2016 = pd.DataFrame(data[data['Date'].str.contains('2016-')])
    Stocks_2017 = pd.DataFrame(data[data['Date'].str.contains('2017-')])
    Stocks_2018 = pd.DataFrame(data[data['Date'].str.contains('2018-')])
    
    frames = [Stocks_2006, Stocks_2007, Stocks_2008, Stocks_2009, Stocks_2010, Stocks_2011, Stocks_2012, Stocks_2013,
              Stocks_2014, Stocks_2015, Stocks_2016, Stocks_2017, Stocks_2018]
    
    Resulting_Data = pd.concat(frames)
    print("Total number of days:", len(Resulting_Data))
    return Resulting_Data

def interploation_1d(life_ladder_data, no_of_years, no_of_days, power):
    num = range(0, no_of_years)
    x = np.array(tuple(num))
    y = np.array(life_ladder_data)
    z = np.polyfit(x, y, power)
    f = np.poly1d(z)
    num_1 = no_of_years - 1
    x_new = np.linspace(0, num_1, no_of_days)
    y_new = f(x_new)
    print("The interpolated y-values are:\n", y_new)
    print("Total:", len(y_new), "datapoints generated for this specific diagram.")
    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name='Data',
        marker=dict(
            size=12))
    trace2 = go.Scatter(
        x=x_new,
        y=y_new,
        mode='lines',
        name='Fit')
    annotation = go.Annotation(
        x=1,
        y=1,
        showarrow=False)
    layout = go.Layout(title='Polynomial Fit in Python',
                       annotations=[annotation])
    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)
    return y_new

def combine_the_data_Stocks_n_LL(StocksData, NyrLLData):
    StocksData.reset_index(drop=True)
    StocksData.index = np.arange(1, len(StocksData)+1)
    NyrLLData.reset_index(drop=True)
    NyrLLData.index = np.arange(1, len(StocksData)+1)
    combine = StocksData.join(NyrLLData)
    
    trace = go.Scatter(
        x = combine['Date'],
        y = combine['Daily Life Ladder'])
    data = [trace]
    iplot(data)
    
    return pd.DataFrame(combine)

US_Stocks = pd.read_csv('Data\Stocks\S&P 500 (^GSPC)_2005to2018_daily.csv')
China_Stocks = pd.read_csv('Data\Stocks\SSE Composite Index (^SSEC)_2006to2017_daily.csv').dropna()
India_Stocks = pd.read_csv('Data\Stocks\S&P BSE SENSEX (^BSESN)_2006to2018.csv').dropna()
Swiss_Stocks = pd.read_csv('Data\Stocks\SMI PR (^SSMI)_2006to2018_daily.csv').dropna()
Japan_Stocks = pd.read_csv(r'Data\Stocks\Nikkei 225 (^N225)_2005to2018_daily.csv').dropna()

model_happiness_US = load_model(stock_prediction_happiness_US.h5)
model_happiness_China = load_model(stock_prediction_happiness_China.h5)
model_happiness_india = load_model(stock_prediction_happiness_india.h5)
model_happiness_Swiss = load_model(stock_prediction_happiness_Swiss.h5)
model_happiness_Japan = load_model(stock_prediction_happiness_Japan.h5)


if __name__ == "__main__":
     