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





app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stock")
def stock():

    df = pd.read_csv("result2.csv")
    df = df.dropna()

    # print(df.head())
   
    dfdict = df.to_dict(orient="record")

    return jsonify(dfdict)
@app.route("/sectors")
def sectors():
    """Return a list of sector names."""
    df = pd.read_csv("result2.csv")
    df = df.dropna()
    sectors = df.Sector.unique().tolist()
    # Return a list of the column names (sample names)
    return jsonify(list(sectors))

@app.route("/year")
def year():
    df = pd.read_csv("result2.csv")
    df = df.dropna()
    year = df.Year.unique().tolist()
    return jsonify(list(year))
    # stock_data = df.loc(df[data] > 1, "Year", )

    # sectors = df.Sector.unique().tolist()
    # years = df.Year.unique()[0::2]
    
    
    
    # dfdict2 = df.to_dict(orient="record")
    # return jsonify(dfdict2)



if __name__ == "__main__":
    app.run(debug=True, port=5003)