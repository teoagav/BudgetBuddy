from flask import Flask
import requests
import json
app = Flask(__name__)


@app.route('/hello')
def hello():
    response = requests.post('https://api.td-davinci.com/api/simulants/search',
        headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ey' +
        'Jpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiZDQyMTg0OWYtODBhMi0zMjZiLWE5YzgtZmI4Zj' +
        'k2MDM3OTVhIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiI4MWEzMjc2MC' +
        '03NTdhLTRlNDAtYmE4ZS04N2EyNDIwNTY3OWEifQ.6_x7VPFdBooncl89XT30nA7_UYM' +
        'MCUrrUiLl3tYmwpE'},
        json = {
            "continuationToken":"",
            "searchCriteria": [
                {"key":"age","operation":">","value":25},
                {"key":"age","operation":"<","value":34}
            ]}
    )
    return response.json()

if __name__ == '__main__':
    app.run()
