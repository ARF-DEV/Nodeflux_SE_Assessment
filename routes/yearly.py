import requests
from flask import Blueprint
from flask import request
from .utils.utils import check_costum_routes, get_yearly_data

yearly_route = Blueprint("yearly", __name__)

@yearly_route.route("/")
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

@yearly_route.route('/<year>')
def get_year(year):

    if not check_costum_routes([year]):
        return {
            "ok" : False,
            "message" : "Invalid route"
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