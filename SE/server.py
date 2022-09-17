from random import randrange

from flask.json import jsonify
from flask import Flask, render_template
from flask import request

import pandas as pd

# n = "dataSets/countrydata.csv"
# data = pd.read_csv(n)
# date_list = list(data[data['countryName'] == '中国']['dateId'])
# countrylist = list(data[data['dateId'] == 20200412]['countryName'])
# countrylist = ['中国'] + countrylist
# print(date_list)
# print(countrylist)

app = Flask(__name__, static_folder="templates")


@app.route("/")
def index():
    return render_template("homepage.html", )


if __name__ == "__main__":
    app.run()
