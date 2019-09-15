import requests
import pymongo
import random
import copy

authKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkI' \
'joiZDQyMTg0OWYtODBhMi0zMjZiLWE5YzgtZmI4Zjk2MDM3OTVhIiwiZXhwIjo5MjIzMzcyMDM2O' \
'DU0Nzc1LCJhcHBfaWQiOiI4MWEzMjc2MC03NTdhLTRlNDAtYmE4ZS04N2EyNDIwNTY3OWEifQ.6_' \
'x7VPFdBooncl89XT30nA7_UYMMCUrrUiLl3tYmwpE'

# Fake Data for Demo
idNumber = 0
paninoTransactionTemplate = {
    'locationLongitude': -80.5402767,
    'locationCountry': 'CA',
    'merchantCategoryCode': '5814',
    'description': 'MR PANINOS #900 _F',
    'type': 'CreditCardTransaction',
    'merchantName': 'Mr Paninos Beijing House',
    'currencyAmount': 'TO INSERT',
    'locationRegion': 'ON',
    'source': 'POS',
    'locationCity': 'Waterloo',
    'originationDateTime': 'TO INSERT',
    'locationPostalCode': 'N2L 3E9',
    'customerId': 'TO INSERT',
    'merchantId': '123-panino',
    'locationLatitude': 43.4721463,
    'id': 'TO INSERT',
    'locationStreet': '106 University Avenue W',
    'accountId': 'TO INSERT',
    'categoryTags': [
      'Food and Dining'
    ]
}

bkTransactionTemplate = {
    'locationLongitude': -80.5466833,
    'locationCountry': 'CA',
    'merchantCategoryCode': '5814',
    'description': 'BK #900 _F',
    'type': 'CreditCardTransaction',
    'merchantName': 'Burger King',
    'currencyAmount': 'TO INSERT',
    'locationRegion': 'ON',
    'source': 'POS',
    'locationCity': 'Waterloo',
    'originationDateTime': 'TO INSERT',
    'locationPostalCode': 'N2L 3E4',
    'customerId': 'TO INSERT',
    'merchantId': '123-bk',
    'locationLatitude': 43.4722488,
    'id': 'TO INSERT',
    'locationStreet': '150 University Avenue W',
    'accountId': 'TO INSERT',
    'categoryTags': [
      'Food and Dining'
    ]
}


# Start the DB
applicationClient = pymongo.MongoClient('mongodb://localhost:27017/')
applicationClient.drop_database('budgetBuddy') # Clear previous data
applicationDb = applicationClient['budgetBuddy']
transactionsCol = applicationDb['transactions']
customersCol = applicationDb['customers']
print(applicationClient.list_database_names())

# Populate the database
customersPerAgeGroup = 10
customersPerSearch = 10
ages = [
    [12, 18],
    [19, 24],
    [25, 34],
    [35, 44],
    [45, 54],
    [55, 64]
]

# Loop through the age groups and search up customer data for each one
for agePair in ages:
    print('Ages ' + str(agePair[0]) + ' to ' + str(agePair[1]))
    continuationToken = ''
    for i in range(int(customersPerAgeGroup / customersPerSearch)):
        response = requests.post('https://api.td-davinci.com/api/simulants/search',
            headers = { 'Authorization': authKey},
            json = {
                'continuationToken': continuationToken,
                'searchCriteria': [
                    {'key':'age','operation':'>','value':agePair[0]},
                    {'key':'age','operation':'<','value':agePair[1]}
                ]
            }
        )

        responseObject = response.json()
        continuationToken = responseObject['result']['continuationToken']
        customers = responseObject['result']['customers']
        customersCol.insert_many(customers)

        customerIds = []
        customerAccountIds = []
        for customer in customers:
            customerIds.append(customer['id'])
            customerAccountIds.append(customer['bankAccounts'][0]['id'])
        print('Ids of inserted customers: ' + str(customerIds))

        # Populate with data from API
        for customerId in customerIds:
            response = requests.get(
                'https://api.td-davinci.com/api/customers/' + customerId + '/transactions',
                headers = { 'Authorization': authKey}
            )
            responseObject = response.json()
            transactions = responseObject['result']
            transactionsCol.insert_many(transactions)

        # Populate with my fake data for demo
        for i in range(len(customerIds)):
            customerId = customerIds[i]
            customerAccountId = customerAccountIds[i]
            paninoTransactionTemplate['customerId'] = customerId
            paninoTransactionTemplate['accountId'] = customerAccountId
            bkTransactionTemplate['customerId'] = customerId
            bkTransactionTemplate['accountId'] = customerAccountId
            dates = [ '2019-09-14T17:35:00Z', '2019-08-14T17:35:00Z', '2019-07-14T17:35:00Z' ]

            for date in dates:
                idNumber += 1
                if random.randint(0,1) == 1:
                    paninosCost = float(random.randint(700,1800)) / 100

                    paninoTransactionTemplate['id'] = 'panino#' + str(idNumber)
                    paninoTransactionTemplate['originationDateTime'] = date
                    paninoTransactionTemplate['currencyAmount'] = paninosCost

                    paninoObject = copy.deepcopy(paninoTransactionTemplate)
                    transactionsCol.insert_one(paninoObject)
                else:
                    bkCost = float(random.randint(1000,2000)) / 100

                    bkTransactionTemplate['id'] = 'bk#' + str(idNumber)
                    bkTransactionTemplate['originationDateTime'] = date
                    bkTransactionTemplate['currencyAmount'] = bkCost

                    bkObject = copy.deepcopy(bkTransactionTemplate)
                    transactionsCol.insert_one(bkObject)
