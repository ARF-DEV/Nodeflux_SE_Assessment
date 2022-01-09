import requests
from flask import Blueprint, make_response

index_route = Blueprint("index", __name__)

@index_route.route("/")
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
    return make_response(response, 200) 