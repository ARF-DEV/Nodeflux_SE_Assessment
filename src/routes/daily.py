import requests
from flask import Blueprint, make_response
from flask import request
from .utils.utils import check_costum_routes, get_daily_data, validate_daily_parameters

daily_route = Blueprint("daily", __name__)

@daily_route.route('/')
def daily():
    
    since = ["2020", "03", "02"] if request.args.get('since') == None else request.args.get('since').split('.')
    upto  = ["2022", "01", "07"] if request.args.get('upto') == None else request.args.get('upto').split('.')

    if not validate_daily_parameters(since):
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }, 400)
    if not validate_daily_parameters(upto):
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'upto' is not valid"
        }, 400)

    since_int = int(''.join(since))
    upto_int = int(''.join(upto))

    if since_int > upto_int:
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }, 400)
    daily_data = get_daily_data()

    response = []
    for current_day_data in daily_data:
        day_int = int(''.join(current_day_data['date'].split('-')))
        if day_int >= since_int and day_int <= upto_int:
            response.append(current_day_data)
        
    return make_response({
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }, 200)


@daily_route.route('/<year>')
def daily_data_by_year(year):
    
    if not check_costum_routes([year]):
        return make_response({
            "ok" : False,
            "message" : "Invalid route"
        }, 400)

    since = [year, "01", "01"] if request.args.get('since') == None else request.args.get('since').split('.')
    upto  = [year, "12", "31"] if request.args.get('upto') == None else request.args.get('upto').split('.')

    if not validate_daily_parameters(since):
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }, 400)
    if not validate_daily_parameters(upto):
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'upto' is not valid"
        }, 400)
    
    if since[0] != year or upto[0] != year:
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'since' and 'upto' must have the same year as the endpoint"
        }, 400)

    since_int = int(''.join(since))
    upto_int = int(''.join(upto))

    if since_int > upto_int:
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }, 400)
    
    daily_data = get_daily_data()
    response = []
    for current_day_data in daily_data:
        day_int = int(''.join(current_day_data['date'].split('-')))
        
        if day_int >= since_int and day_int <= upto_int:
            response.append(current_day_data)
        
    return make_response({
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }, 200)

@daily_route.route('/<year>/<month>')
def daily_data_by_year_and_month(year, month):
    routes = [year,month]
    if not check_costum_routes(routes):
        return make_response({
            "ok" : False,
            "message" : "Invalid route"
        }, 400)
    
    
    since = [year, month, "01"] if request.args.get('since') == None else request.args.get('since').split('.')
    upto  = [year, month, "31"] if request.args.get('upto') == None else request.args.get('upto').split('.')

    if not validate_daily_parameters(since):
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'since' is not valid"
        }, 400)
    if not validate_daily_parameters(upto):
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'upto' is not valid"
        }, 400)

    if since[0] != routes[0] or since[1] != routes[1] or upto[0] != routes[0] or upto[1] != routes[1]:
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'since' and 'upto' must have the same year and month as the endpoint"
        }, 400)
    since_int = int(''.join(since))
    upto_int = int(''.join(upto))

    if since_int > upto_int:
        return make_response({
            "ok" : False,
            "message" : "Query parameter 'since' cannot be larger than 'upto'"
        }, 400)
    
    daily_data = get_daily_data()
    response = []
    for current_day_data in daily_data:
        day_int = int(''.join(current_day_data['date'].split('-')))
        
        if day_int >= since_int and day_int <= upto_int:
            response.append(current_day_data)
        
    return make_response({
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }, 200)

@daily_route.route('/<year>/<month>/<date>')
def daily_data_by_date(year, month, date):
    routes = [year,month, date]
    if not check_costum_routes(routes):
        return make_response({
            "ok" : False,
            "message" : "Invalid route"
        }, 400)
    
    daily_data = get_daily_data()
    response = {}
    date_wanted = '-'.join(routes)
    for current_day_data in daily_data:

        if current_day_data['date'] == date_wanted:
            response = current_day_data
            break
        
    return make_response({
        "ok" : True,
        "data" : response,
        "message" : "Data fetch success"
    }, 200)