from flask import Flask, render_template, jsonify, request, redirect, url_for
from random import sample

import numpy as np 
import json
import pandas as pd

df = pd.read_csv("data/Influenza_NY.csv")
returned_data = {}

app = Flask(__name__)

def getAll_counties():
    all_counties = list(df["County"].unique())
    return all_counties

@app.route('/', methods = ["GET"])
def index():
    all_data = df.to_dict(orient='records')
    all_data = json.dumps(all_data, indent=2)
    all_counties = getAll_counties()
    returned_data["all_data"] = all_data
    returned_data["all_counties"] = json.dumps(all_counties)
    return render_template("index.html", returned_data = returned_data)
    
if __name__ == '__main__':
    app.run(debug=True)