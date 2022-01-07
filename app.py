import requests
from flask import Flask
from flask import jsonify
from flask import request

from utils import get_monthly_data, get_yearly_data, validate_monthly_parameters, get_daily_data, validate_daily_parameters, check_costum_routes

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
            "message" : "Query parameters is invalid"
        }

    if since > upto :
        return {
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }

    if since < 0 or upto < 0:
        return {
            "ok" : False,
            "message" : "Query parameters cannot be a negative number"
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

    if not check_costum_routes([year]):
        return {
            "ok" : False,
            "message" : "Invalid route"
        }

    if year < 0 :
        return {
            "ok" : False,
            "message" : "The endpoint cannot be negative number"
        }

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
    
    if not validate_monthly_parameters(since) :
        return {
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }
    
    if not validate_monthly_parameters(upto) :
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
    if not check_costum_routes([year]):
        return {
            "ok" : False,
            "message" : "Invalid route"
        }

    since = [year, "01"] if request.args.get('since') == None else request.args.get('since').split('.')
    upto  = [year,"12"] if request.args.get('upto') == None else request.args.get('upto').split('.')
    
    if not validate_monthly_parameters(since) :
        return {
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }
    
    if not validate_monthly_parameters(upto):
        return {
            "ok" : False,
            "message" : "Query parameter 'upto' is not valid"
        }

    if since[0] != year or upto[0] != year:
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
        month_int = int(''.join(current_month_data['month'].split('-')))
        
        if month_int >= since_int and month_int <= upto_int:
            response.append(current_month_data)
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }

@app.route('/monthly/<year>/<month>')
def get_specific_month(year, month):
    custom_routes = [year, month]
    if not check_costum_routes(custom_routes):
        return {
            "ok" : False,
            "message" : "Route is not valid"
        }
    result = get_monthly_data()
    response = {}
    month_wanted_int = '-'.join(custom_routes)
    for current_month_data in result:

        if month_wanted_int == current_month_data['month']:
            response = current_month_data
            break
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }

@app.route('/daily')
def daily():
    
    since = ["2020", "03", "02"] if request.args.get('since') == None else request.args.get('since').split('.')
    upto  = ["2022", "01", "07"] if request.args.get('upto') == None else request.args.get('upto').split('.')

    if not validate_daily_parameters(since):
        return {
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }
    if not validate_daily_parameters(upto):
        return {
            "ok" : False,
            "message" : "Query parameter 'upto' is not valid"
        }

    since_int = int(''.join(since))
    upto_int = int(''.join(upto))

    if since_int > upto_int:
        return {
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }
    daily_data = get_daily_data()


    response = []
    for current_day_data in daily_data:
        day_int = int(''.join(current_day_data['date'].split('-')))
        
        if day_int >= since_int and day_int <= upto_int:
            response.append(current_day_data)
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }


@app.route('/daily/<year>')
def daily_data_by_year(year):
    
    if not check_costum_routes([year]):
        return {
            "ok" : False,
            "message" : "Invalid route"
        }

    since = ["2020", "03", "02"] if request.args.get('since') == None else request.args.get('since').split('.')
    upto  = ["2022", "01", "07"] if request.args.get('upto') == None else request.args.get('upto').split('.')

    if not validate_daily_parameters(since):
        return {
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }
    if not validate_daily_parameters(upto):
        return {
            "ok" : False,
            "message" : "Query parameter 'upto' is not valid"
        }
    
    if since[0] != year or upto[0] != year:
        return {
            "ok" : False,
            "message" : "Query parameter 'since' and 'upto' must have the same year as the endpoint"
        }

    since_int = int(''.join(since))
    upto_int = int(''.join(upto))

    if since_int > upto_int:
        return {
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }
    
    daily_data = get_daily_data()
    response = []
    for current_day_data in daily_data:
        day_int = int(''.join(current_day_data['date'].split('-')))
        
        if day_int >= since_int and day_int <= upto_int:
            response.append(current_day_data)
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }

@app.route('/daily/<year>/<month>')
def daily_data_by_year_and_month(year, month):
    routes = [year,month]
    if not check_costum_routes(routes):
        return {
            "ok" : False,
            "message" : "Invalid route"
        }
    
    
    since = ["2020", "03", "02"] if request.args.get('since') == None else request.args.get('since').split('.')
    upto  = ["2022", "01", "07"] if request.args.get('upto') == None else request.args.get('upto').split('.')

    if not validate_daily_parameters(since):
        return {
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }
    if not validate_daily_parameters(upto):
        return {
            "ok" : False,
            "message" : "Query parameter 'upto' is not valid"
        }

    if since[0] != routes[0] or since[1] != routes[1] or upto[0] != routes[0] or upto[1] != routes[1]:
        return {
            "ok" : False,
            "message" : "Query parameter 'since' and 'upto' must have the same year and month as the endpoint"
        }
    since_int = int(''.join(since))
    upto_int = int(''.join(upto))

    if since_int > upto_int:
        return {
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }
    
    daily_data = get_daily_data()
    response = []
    for current_day_data in daily_data:
        day_int = int(''.join(current_day_data['date'].split('-')))
        
        if day_int >= since_int and day_int <= upto_int:
            response.append(current_day_data)
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }

@app.route('/daily/<year>/<month>/<date>')
def daily_data_by_date(year, month, date):
    routes = [year,month, date]
    if not check_costum_routes(routes):
        return {
            "ok" : False,
            "message" : "Invalid route"
        }
    
    daily_data = get_daily_data()
    response = {}
    date_wanted = '-'.join(routes)
    for current_day_data in daily_data:

        if current_day_data['date'] == date_wanted:
            response = current_day_data
            break
        
    return {
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }