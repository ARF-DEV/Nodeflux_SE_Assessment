import requests
from flask import Flask
from flask import jsonify
from flask import request

from utils import get_monthly_data, get_yearly_data, validate_parameters_monthly

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
    
    since = ["2020", "03"] if request.args.get('since') == None else request.args.get('since').split('.')
    upto  = ["2022","01"] if request.args.get('upto') == None else request.args.get('upto').split('.')
    
    if not validate_parameters_monthly(since, 2) :
        return {
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }
    
    if not validate_parameters_monthly(upto, 2) :
        return {
            "ok" : False,
            "message" : "Query parameter 'upto' is not valid"
        }

    # ex. ["2021", "03"] -> 202103
    #                       ^^^^..
    # digits above ^ symbol is the year
    # digits above . symbol is the month
    # if the year is the same (ex. 202104 and 202103) it will compare month digit only
    # if the year is different (ex. 202004 and 202201) the month side wont matter 
    # because the number on year side are more significant than on the month side 
    since_int = int(''.join(since))
    upto_int = int(''.join(upto))

    if since_int > upto_int:
        return {
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }


    result = get_monthly_data()
    response = []
    save = False
    for current_month_data in result:
        if current_month_data['month'] == '-'.join(since):
            save = True
        
        if save:
            response.append(current_month_data)
        
        if current_month_data['month'] == '-'.join(upto):
            save = False
        
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }

@app.route('/monthly/<year>')
def monthly_in_a_year(year):
    since = [year, "01"] if request.args.get('since') == None else request.args.get('since').split('.')
    upto  = [year,"12"] if request.args.get('upto') == None else request.args.get('upto').split('.')
    
    if not validate_parameters_monthly(since, 2) :
        return {
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }
    
    if not validate_parameters_monthly(upto, 2) :
        return {
            "ok" : False,
            "message" : "Query parameter 'upto' is not valid"
        }

    if int(since[0]) != year and int(upto[0]) != year:
        return {
            "ok" : False,
            "message" : "Query parameter 'since' and 'upto' must have the same year as the endpoint"
        }

    # ex. ["2021", "03"] -> 202103
    #                       ^^^^..
    # digits above ^ symbol is the year
    # digits above . symbol is the month
    # if the year is the same (ex. 202104 and 202103) it will compare month digit only
    # if the year is different (ex. 202004 and 202201) the month side wont matter 
    # because the number on year side are more significant than on the month side 
    since_int = int(''.join(since))
    upto_int = int(''.join(upto))

    if since_int > upto_int:
        return {
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }
    
    result = get_monthly_data()
    response = []
    for current_month_data in result:
        date_int = int(''.join(current_month_data['month'].split('-')))
        
        if date_int >= since_int and date_int <= upto_int:
            response.append(current_month_data)
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }

@app.route('/monthly/<year>/<month>')
def get_specific_month(year, month):
    try:
        int(year)
    except ValueError:
        return {
            "ok" : False,
            "message" : "year is not valid"
        }

    try:
        int(month)
    except ValueError:
        return {
            "ok" : False,
            "message" : "month is not valid"
        }


    if int(month) < 1 or int(month) > 31:
        return {
                "ok" : False,
                "message" : "month must be >= 1 or <= 31"
            }

    result = get_monthly_data()
    response = {}
    date_wanted_int = int(''.join([year, month]))
    for current_month_data in result:
        date_int = int(''.join(current_month_data['month'].split('-')))
        
        if date_wanted_int == date_int:
            response = current_month_data
            break
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }