import requests
import pymongo

# Start the DB
applicationClient = pymongo.MongoClient('mongodb://localhost:27017/')
applicationDb = applicationClient['budgetBuddy']
print(applicationClient.list_database_names())

customersCol = applicationDb['customers']

# Populate the database
customersPerAgeGroup = 100
customersPerSearch = 10
ages = [
    [12, 18],
    [19, 24],
    [25, 34],
    [35, 44],
    [45, 54],
    [55, 64]
]

# Loop through the age groups and seach up customer data for each one
for agePair in ages:
    print('Ages ' + str(agePair[0]) + ' to ' + str(agePair[1]))
    continuationToken = ''
    for i in range(int(customersPerAgeGroup / customersPerSearch)):
        response = requests.post('https://api.td-davinci.com/api/simulants/search',
            headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ey' +
            'Jpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiZDQyMTg0OWYtODBhMi0zMjZiLWE5YzgtZmI4Zj' +
            'k2MDM3OTVhIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiI4MWEzMjc2MC' +
            '03NTdhLTRlNDAtYmE4ZS04N2EyNDIwNTY3OWEifQ.6_x7VPFdBooncl89XT30nA7_UYM' +
            'MCUrrUiLl3tYmwpE'},
            json = {
                'continuationToken': continuationToken,
                'searchCriteria': [
                    {'key':'age','operation':'>','value':agePair[0]},
                    {'key':'age','operation':'<','value':agePair[1]}
                ]
            }
        )

        responseObject = response.json()
        customers = responseObject['result']['customers']
        ids = customersCol.insert_many(customers)
        print('Ids of inserted customers: ' + str(ids.inserted_ids))

        continuationToken = responseObject['result']['continuationToken']

#TODO persist the db
applicationClient.drop_database('mydatabase')
