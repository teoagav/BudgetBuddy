from flask import Flask
import requests
app = Flask(__name__)


@app.route('/hello')
def hello():
    response = requests.get('https://api.td-davinci.com/api/branches',
    headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3' +
    'MiOiJDQlAiLCJ0ZWFtX2lkIjoiZDQyMTg0OWYtODBhMi0zMjZiLWE5YzgtZmI4Zjk2MDM3OT' +
    'VhIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiI4MWEzMjc2MC03NTdhLTRlND' +
    'AtYmE4ZS04N2EyNDIwNTY3OWEifQ.6_x7VPFdBooncl89XT30nA7_UYMMCUrrUiLl3tYmwpE' }
    )
    return response.json()

if __name__ == '__main__':
    app.run()
