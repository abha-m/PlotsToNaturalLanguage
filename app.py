from flask import Flask, render_template, jsonify, request, redirect, url_for
from random import sample
from sklearn import preprocessing

import numpy as np 
import json
import pandas as pd

df = pd.read_csv("data/Influenza_NY.csv")
df = df.dropna()
df = df.drop('Unnamed: 0', axis=1)
numeric_cols = list(df.corr().columns)
returned_data = {}

app = Flask(__name__)

def getAll_counties():
    all_counties = list(df["County"].unique())
    return all_counties

@app.route('/', methods = ["GET", "POST"])
def index():
    returned_data['all_data'] = df.to_dict(orient='records')
    return render_template("index.html", returned_data = returned_data)

@app.route('/county/<county_name>', methods = ["GET", "POST"])
def filter_by_county(county_name):
    if county_name not in returned_data:
        filtered_by_county_df = df[df["County"] == county_name]
        filtered_by_county_df = filtered_by_county_df.to_dict(orient='records')
        returned_data[county_name] = filtered_by_county_df
        x = filtered_by_county_df[numeric_cols].values #returns a numpy array
        min_max_scaler = preprocessing.StandardScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        scaled_filtered = pd.DataFrame(x_scaled, columns=numeric_cols)
        df.corr().fillna(0).to_csv("test.csv")
    return json.dumps(returned_data)
    
if __name__ == '__main__':
    app.run(debug=True)