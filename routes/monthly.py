import requests
from flask import Blueprint
from flask import request
from .utils.utils import check_costum_routes, get_monthly_data, validate_monthly_parameters

monthly_route = Blueprint("monthly", __name__)

@monthly_route.route('/')
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

@monthly_route.route('/<year>')
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

@monthly_route.route('/<year>/<month>')
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