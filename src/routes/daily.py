import requests
from flask import Blueprint
from flask import request
from .utils.utils import check_costum_routes, get_daily_data, validate_daily_parameters

daily_route = Blueprint("daily", __name__)

@daily_route.route('/')
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


@daily_route.route('/<year>')
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

@daily_route.route('/<year>/<month>')
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

@daily_route.route('/<year>/<month>/<date>')
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