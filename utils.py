import requests

def get_monthly_data():
    api_res = requests.get("https://data.covid19.go.id/public/api/update.json")
    json_data_update = api_res.json()['update']
    
    daily_data = json_data_update['harian']

    year_month_of_current_data = ''
    previous_data, year_month_of_previous_data = daily_data[0], daily_data[0]['key_as_string'].split('-')[1]

    positive, recovered, deaths, active = daily_data[0]['jumlah_positif']['value'], daily_data[0]['jumlah_sembuh']['value'], daily_data[0]['jumlah_meninggal']['value'], daily_data[0]['jumlah_dirawat']['value']
    
    result = []
    for current_data in daily_data[1:]:
        key_as_string = current_data['key_as_string']
        split_key = key_as_string.split('-')
        year_month_of_current_data = f"{split_key[0]}-{split_key[1]}"
        
        if year_month_of_previous_data != year_month_of_current_data:
            last_month_data = {
                'month' : year_month_of_previous_data,
                'positive': positive,
                'recovered': recovered,
                'deaths': deaths,
                'active': active,
            }
            positive, recovered, deaths, active = 0, 0, 0, 0
            result.append(last_month_data)

        positive += current_data['jumlah_positif']['value']
        recovered += current_data['jumlah_sembuh']['value']
        deaths += current_data['jumlah_meninggal']['value']
        active += current_data['jumlah_dirawat']['value']

        previous_data = current_data
        year_month_of_previous_data = year_month_of_current_data
    
    last_month_data = {
                'month' : year_month_of_previous_data,
                'positive': positive,
                'recovered': recovered,
                'deaths': deaths,
                'active': active,
            }
    result.append(last_month_data)
    return result

def get_yearly_data():
    api_res = requests.get("https://data.covid19.go.id/public/api/update.json")
    json_data_update = api_res.json()['update']
    
    daily_data = json_data_update['harian']

    year_of_current_data = ''
    previous_data, year_of_previous_data = daily_data[0], daily_data[0]['key_as_string'].split('-')[0]

    positive, recovered, deaths, active = daily_data[0]['jumlah_positif']['value'], daily_data[0]['jumlah_sembuh']['value'], daily_data[0]['jumlah_meninggal']['value'], daily_data[0]['jumlah_dirawat']['value']
    
    result = []
    for current_data in daily_data[1:]:
        key_as_string = current_data['key_as_string']
        split_key = key_as_string.split('-')
        year_of_current_data = split_key[0]
        
        if year_of_previous_data != year_of_current_data:
            last_year_data = {
                'year' : year_of_previous_data,
                'positive': positive,
                'recovered': recovered,
                'deaths': deaths,
                'active': active,
            }
            positive, recovered, deaths, active = 0, 0, 0, 0
            result.append(last_year_data)

        positive += current_data['jumlah_positif']['value']
        recovered += current_data['jumlah_sembuh']['value']
        deaths += current_data['jumlah_meninggal']['value']
        active += current_data['jumlah_dirawat']['value']

        previous_data = current_data
        year_of_previous_data = year_of_current_data
    
    last_year_data = {
                'year' : year_of_previous_data,
                'positive': positive,
                'recovered': recovered,
                'deaths': deaths,
                'active': active,
            }
    result.append(last_year_data)

    return result



def validate_monthly_parameters(params):
    if len(params) != 2:
        print('A')
        return False
    else:
        try:
            if int(params[0]) < 0:
                print('B')
                return False
            if int(params[1]) < 1 or int(params[1]) > 12:
                print('C')
                return False
        except ValueError:
            print('D')
            return False
        
        if len(params[1]) == 1 :
            params[1] = '0' + params[1]
    

        return True

def validate_daily_parameters(params):
    if len(params) != 3:
        return False
    else:
        try:
            if int(params[0]) < 0:
                return False
            if int(params[1]) < 1 or int(params[1]) > 12:
                return False
            if int(params[2]) < 1 or int(params[2]) > 31:
                return False
        except ValueError:
            return False
        
        if len(params[1]) == 1 :
            params[1] = '0' + params[1]
        if len(params[2]) == 1 :
            params[2] = '0' + params[2]
    

        return True


def get_daily_data() :
    api_res = requests.get("https://data.covid19.go.id/public/api/update.json")
    json_data_update = api_res.json()['update']
    
    per_day_data = json_data_update['harian']

    result = []
    for data in per_day_data:
        key_string = data['key_as_string']
        cur_date = key_string.split('T')[0]
        
        result.append({
            "date": cur_date,
            "positive": data['jumlah_positif']['value'],
            "recovered": data['jumlah_sembuh']['value'],
            "deaths": data['jumlah_meninggal']['value'],
            "active": data['jumlah_dirawat']['value'],
        })

    return result

def check_costum_routes(routes):
    try:
        for i in range(len(routes)):
            int(routes[i])
            if len(routes[i]) == 1:
                routes[i] = '0' + routes[i]
    except ValueError:
        return False
    
    return True
