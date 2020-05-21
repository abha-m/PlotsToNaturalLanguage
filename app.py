from flask import Flask, render_template, jsonify, request, redirect, url_for
from random import sample
from sklearn import preprocessing
from simplenlg import Lexicon
from simplenlg import NLGFactory
from simplenlg import Realiser

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

@app.route('/request', methods = ["GET", "POST"])
def filter_by_county():
    county_name = request.args.get('county')
    selected_attributes = request.args.getlist('attributes')
    print(county_name)
    print(selected_attributes)
    if county_name not in returned_data:
        filtered_by_county_df = df[df["County"] == county_name]
        # filtered_by_county_df = filtered_by_county_df.to_dict(orient='records')
        # returned_data[county_name] = filtered_by_county_df
        x = filtered_by_county_df[numeric_cols].values #returns a numpy array
        min_max_scaler = preprocessing.StandardScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        scaled_filtered = pd.DataFrame(x_scaled, columns=numeric_cols)
        correlation_matrix_df = scaled_filtered.corr().fillna(0)
        correlation_matrix_df["Attribute"] = correlation_matrix_df.keys()
        correlation_matrix_df_filtered = correlation_matrix_df[selected_attributes + ["Attribute"]]
        returned_data["correlation"] = correlation_matrix_df_filtered.to_dict(orient='records')
        returned_data["scatterplot"] = filtered_by_county_df[selected_attributes].to_dict(orient='records')
        returned_data["scatterplot_matrix"] = filtered_by_county_df[selected_attributes].to_dict(orient='records')
        returned_data["scatterplot_matrix_text1"] = str(generateStory(["Year", "Population"], correlation_matrix_df["Year"]["Population"]))
        returned_data["scatterplot_matrix_text2"] = str(generateStory(["Year", "Unemp_rate"], correlation_matrix_df["Year"]["Unemp_rate"]))
        returned_data["scatterplot_matrix_text3"] = str(generateStory(["Population", "Unemp_rate"], correlation_matrix_df["Population"]["Unemp_rate"]))
    return json.dumps(returned_data)

def generateStory(words, correlation_value):
    lexicon = Lexicon.getDefaultLexicon()
    nlgFactory = NLGFactory(lexicon)
    realiser = Realiser(lexicon)


    start_s = nlgFactory.createClause("From the above scatterplot matrix we observe that")


    if correlation_value > 0:
        # positive correlation
        s1 = nlgFactory.createClause("there is a positive correlation between the attributes, " +words[0]+ " and " +words[1])
    elif correlation_value < 0:
        # negative correlation
        s1 = nlgFactory.createClause("there is a negative correlation between the attributes, " +words[0]+ " and " +words[1])
    elif correlation_value == 0:
        # no correlation
        s1 = nlgFactory.createClause("there is a no correlation between the attributes, " +words[0]+ " and " +words[1])


    if correlation_value > 0.4 or correlation_value < -0.4:
        # high correlation
        s2 = nlgFactory.createClause("the correlation between these attributes is high")
    else:
        # low correlation
        s2 = nlgFactory.createClause("the correlation between these attributes is low")


    # combine the sentences to generate a story
    phrase_element = nlgFactory.createCoordinatedPhrase()
    phrase_element.addCoordinate(start_s)
    phrase_element.addCoordinate(s1)
    phrase_element.addCoordinate(s2)


    story = realiser.realiseSentence(phrase_element)
    return story
    # print(story)
    
if __name__ == '__main__':
    app.run(debug=True)