import requests
from flask import Flask
from flask import jsonify
from flask import request

from utils import get_monthly_data, get_yearly_data

app = Flask(__name__)

@app.route("/")
def index() :
    api_res = requests.get("https://data.covid19.go.id/public/api/update.json")
    json_data_update = api_res.json()['update']
    response = {
        "ok": True,
        "data": {
            "total_positive": json_data_update['total']['jumlah_positif'],
            "total_recovered": json_data_update['total']['jumlah_sembuh'],
            "total_deaths": json_data_update['total']['jumlah_meninggal'],
            "total_active": json_data_update['total']['jumlah_dirawat'],
            "new_positive": json_data_update['penambahan']['jumlah_positif'],
            "new_recovered": json_data_update['penambahan']['jumlah_sembuh'],
            "new_deaths": json_data_update['penambahan']['jumlah_meninggal'],
            "new_active": json_data_update['penambahan']['jumlah_dirawat'],
        },
        "message" : "Data fetch success"
    }
    return response

@app.route("/yearly")
def yearly():

    try:
        since = 2020 if request.args.get('since') == None else int(request.args.get('since'))
        upto  = 2022 if request.args.get('upto') == None else int(request.args.get('upto'))
    except ValueError:
        return {
            "ok" : False,
            "message" : "Query parameters cannot be converted to integer"
        }

    if since > upto :
        return {
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }

    result = get_yearly_data()
    response = []

    for current_year_data in result:
        year = int(current_year_data['year'])
        if year >= since and year <= upto :
            response.append(current_year_data) 

    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }

@app.route('/yearly/<year>')
def get_year(year):
    result = get_yearly_data()
    response = {}
    for current_year_data in result:
        if year == current_year_data['year'] :
            response = current_year_data
            break

    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }


@app.route('/monthly')
def monthly():
    
    try:
        since = "2020-03" if request.args.get('since') == None else '-'.join(request.args.get('since').split('.'))
        upto  = "2022-01" if request.args.get('upto') == None else '-'.join(request.args.get('upto').split('.'))
    except ValueError:
        return {
            "ok" : False,
            "message" : "Query parameters cannot be converted to integer"
        }


    # ex. 2021-03 -> 202103
    #                ^^^^..
    # digits above ^ symbol is the year
    # digits above . symbol is the month
    # if the year is the same (ex. 202104 and 202103) it will compare month digit only
    # if the year is different (ex. 202004 and 202201) the month side wont matter 
    # because the number on year side are more significant than on the month side 
    since_int = int(''.join(since.split('-')))
    upto_int = int(''.join(upto.split('-')))

    print(since_int, upto_int)
    if since_int > upto_int:
        return {
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }


    result = get_monthly_data()
    response = []
    save = False
    for current_month_data in result:
        if current_month_data['month'] == since:
            save = True
        
        if save:
            response.append(current_month_data)

        if current_month_data['month'] == upto:
            save = False
        
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }

