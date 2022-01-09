import unittest
import requests

class ApiTest(unittest.TestCase):
    API_URL = "http://192.168.212.197:8080/"


    def test_index(self):
        res = requests.get(ApiTest.API_URL)
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), {
            "data": {
                "new_active": 316,
                "new_deaths": 2,
                "new_positive": 529,
                "new_recovered": 211,
                "total_active": 6108,
                "total_deaths": 144129,
                "total_positive": 4266195,
                "total_recovered": 4115958
            },
            "message": "Data fetch success",
            "ok": True
        })
    
    def test_yearly(self):
        # default yearly
        res = requests.get(f"{ApiTest.API_URL}yearly")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 3)

        # yearly with query params
        res = requests.get(f"{ApiTest.API_URL}yearly", params={'since':"owakdoawkd", 'upto':"2021"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}yearly", params={'since':"2022", 'upto':"2021"})
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}yearly", params={'since':"-1", 'upto':"2021"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}yearly", params={'since':"2020", 'upto':"2021"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 2)

        # yearly/<year> endpoint
        res = requests.get(f"{ApiTest.API_URL}yearly/asdawd")
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}yearly/2021")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['data']['year'], "2021")
        
        
        

    def test_monthly(self):
        # request without query params
        res = requests.get(f"{ApiTest.API_URL}monthly")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 23)

        # request with query params
        res = requests.get(f"{ApiTest.API_URL}monthly", params={'since':"owakdoawkd", 'upto':"2021.10"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}monthly", params={'since':"2022.4", 'upto':"2021.3"})
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}monthly", params={'since':"2022", 'upto':"2021.3"})
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}monthly", params={'since':"-1", 'upto':"2021.01"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}monthly", params={'since':"2021.02", 'upto':"2021.03"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 2)

        # monthly/<year>
        res = requests.get(f"{ApiTest.API_URL}monthly/2021")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 12)

        res = requests.get(f"{ApiTest.API_URL}monthly/2020", params={'since':"owakdoawkd", 'upto':"2021.10"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}monthly/2020", params={'since':"2022.4", 'upto':"2021.3"})
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}monthly/2020", params={'since':"2022", 'upto':"2021.3"})
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}monthly/2020", params={'since':"-1", 'upto':"2021.01"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}monthly/2020", params={'since':"2021.02", 'upto':"2021.04"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}monthly/2021", params={'since':"2021.02", 'upto':"2021.06"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 5)

        # monthly/<year>/<month>
        res = requests.get(f"{ApiTest.API_URL}monthly/dwadwad/03")
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}monthly/2021/awdasd")
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}monthly/2021/03")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['data']['month'], "2021-03")

    def test_daily(self):
        # request without query params
        res = requests.get(f"{ApiTest.API_URL}daily")
        self.assertEqual(res.status_code, 200)

        # request with query params
        res = requests.get(f"{ApiTest.API_URL}daily", params={'since':"2021.10.3", 'upto':"wadwadwadsa"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily", params={'since':"2022.4", 'upto':"2021.3.1"})
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}daily", params={'since':"2022.4.2", 'upto':"2021.3.1"})
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}daily", params={'since':"-1", 'upto':"2021.01.2"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily", params={'since':"2021.02.3", 'upto':"2021.02.4"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 2)

        # daily/<year>
        res = requests.get(f"{ApiTest.API_URL}daily/2021")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 365)

        res = requests.get(f"{ApiTest.API_URL}daily/2020", params={'since':"owakdoawkd", 'upto':"2021.10.3"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily/2020", params={'since':"2022.4.3", 'upto':"2021.3.3"})
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}daily/2020", params={'since':"2022", 'upto':"2021.3.2"})
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}daily/2020", params={'since':"-1", 'upto':"2021.01"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily/2020", params={'since':"2021.02.3", 'upto':"2021.04.1"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily/2021", params={'since':"2021.02.1", 'upto':"2021.03.1"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 29)

        # daily/<year>/<month>
        res = requests.get(f"{ApiTest.API_URL}daily/dwadwad/03")
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily/2021/awdasd")
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily/2021/03")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 31)

        res = requests.get(f"{ApiTest.API_URL}daily/2021/03", params={'since':"owakdowakd", 'upto':"2020.03.09"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily/2021/03", params={'since':"2020.03.10", 'upto':"2020.03.09"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily/2021/03", params={'since':"2020.03.10", 'upto':"-1"})
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily/2021/03", params={'since':"2021.03.10", 'upto':"2021.03.12"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['data']), 3)

        # daily/<year>/<month>/<day>
        res = requests.get(f"{ApiTest.API_URL}daily/2021/awdadsd/15")
        self.assertEqual(res.status_code, 400)

        res = requests.get(f"{ApiTest.API_URL}daily/2021/-3/15")
        self.assertEqual(res.status_code, 400)
        
        res = requests.get(f"{ApiTest.API_URL}daily/2021/03/15")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['data']['date'], "2021-03-15")


if __name__ == "__main__" :
    unittest.main()