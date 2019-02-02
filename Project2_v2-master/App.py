import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib
# import dash
import plotly
plotly.__version__
import json
# plotly.tools.set_credentials_file(username='Brybtb', api_key='50jVIE7Kj5EttwIAtSyJ')
from plotly.offline import init_notebook_mode, iplot, plot
from IPython.display import display, HTML
from flask import Flask, render_template, url_for, jsonify

# ----------------------------------------------
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF

df = pd.read_csv('result2.csv')

sample_data_table = FF.create_table(df.head(5))
py.iplot(sample_data_table, filename='sample-data-table')

trace1 = go.Scatter(x=df['Ticker'], y=df['PE'],mode='lines', name='')
trace2 = go.Scatter(x=df['Ticker'],y=df['PE'], mode='lines', name='')
trace3 = go.Scatter(x=df['Ticker'],y=df['PE'], mode='lines', name='')
layout = go.Layout(title='Simple Plot from csv data',plot_bgcolor='rgb(230,230,230)')
fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
py.plot(fig,filename='simple-plot-from-csv')

b_df = pd.read_csv('Apple.csv')
b_df_external_source = FF.create_table(b_df.head())
py.plot(b_df_external_source, filename='apple-data')

trace = go.Scatter(x=b_df['Date'], y=b_df['Open'],
                  name='Share Prices')

layout = go.Layout(title="Apple Share Prices", plot_bgcolor='rgb(230,230,230)',showlegend=True)
fig = go.Figure(data=[trace],layout=layout)
py.plot(fig,filename='apple-stock')

