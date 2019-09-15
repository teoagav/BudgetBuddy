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
    'merchantName': 'Mr Panino\'s Beijing House',
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

harveysTransactionTemplate = {
    'locationLongitude': -80.5384454,
    'locationLatitude': 43.4719514,
    'merchantId': '123-harvey',
    'description': 'HARVEY #900 _F',
    'merchantName': 'Harvey\'s',
    'locationStreet': '170 University Avenue W',
    'locationCountry': 'CA',
    'merchantCategoryCode': '5814',
    'type': 'CreditCardTransaction',
    'currencyAmount': 'TO INSERT',
    'locationRegion': 'ON',
    'source': 'POS',
    'locationCity': 'Waterloo',
    'originationDateTime': 'TO INSERT',
    'locationPostalCode': 'N2L 3E4',
    'customerId': 'TO INSERT',
    'id': 'TO INSERT',
    'accountId': 'TO INSERT',
    'categoryTags': [
      'Food and Dining'
    ]
}

subwayTransactionTemplate = {
    'locationLongitude': -80.5375333,
    'locationLatitude': 43.472145,
    'merchantId': '123-subway',
    'description': 'SUBWAY #900 _F',
    'merchantName': 'Subway',
    'locationStreet': '160 University Avenue W',
    'locationCountry': 'CA',
    'merchantCategoryCode': '5814',
    'type': 'CreditCardTransaction',
    'currencyAmount': 'TO INSERT',
    'locationRegion': 'ON',
    'source': 'POS',
    'locationCity': 'Waterloo',
    'originationDateTime': 'TO INSERT',
    'locationPostalCode': 'N2L 3E4',
    'customerId': 'TO INSERT',
    'id': 'TO INSERT',
    'accountId': 'TO INSERT',
    'categoryTags': [
      'Food and Dining'
    ]
}

golsTransactionTemplate = {
    'locationLongitude': -80.5371392,
    'locationLatitude': 43.4725607,
    'merchantId': '123-gol',
    'description': 'GOLS #900 _F',
    'merchantName': 'Gol\'s Lanzhou Noodle',
    'locationStreet': '150 University Avenue W',
    'locationCountry': 'CA',
    'merchantCategoryCode': '5814',
    'type': 'CreditCardTransaction',
    'currencyAmount': 'TO INSERT',
    'locationRegion': 'ON',
    'source': 'POS',
    'locationCity': 'Waterloo',
    'originationDateTime': 'TO INSERT',
    'locationPostalCode': 'N2L 3E4',
    'customerId': 'TO INSERT',
    'id': 'TO INSERT',
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
                if random.randint(0,1) == 1:
                    bkCost = float(random.randint(500,1000)) / 100

                    bkTransactionTemplate['id'] = 'bk#' + str(idNumber)
                    bkTransactionTemplate['originationDateTime'] = date
                    bkTransactionTemplate['currencyAmount'] = bkCost

                    bkObject = copy.deepcopy(bkTransactionTemplate)
                    transactionsCol.insert_one(bkObject)
                if random.randint(0,1) == 1:
                    harveysCost = float(random.randint(900,2100)) / 100

                    harveysTransactionTemplate['id'] = 'harveys#' + str(idNumber)
                    harveysTransactionTemplate['originationDateTime'] = date
                    harveysTransactionTemplate['currencyAmount'] = harveysCost

                    harveysObject = copy.deepcopy(harveysTransactionTemplate)
                    transactionsCol.insert_one(harveysObject)
                if random.randint(0,1) == 1:
                    subwayCost = float(random.randint(1000,2500)) / 100

                    subwayTransactionTemplate['id'] = 'subway#' + str(idNumber)
                    subwayTransactionTemplate['originationDateTime'] = date
                    subwayTransactionTemplate['currencyAmount'] = subwayCost

                    subwayObject = copy.deepcopy(subwayTransactionTemplate)
                    transactionsCol.insert_one(subwayObject)
                if random.randint(0,1) == 1:
                    golsCost = float(random.randint(1500,3000)) / 100

                    golsTransactionTemplate['id'] = 'gols#' + str(idNumber)
                    golsTransactionTemplate['originationDateTime'] = date
                    golsTransactionTemplate['currencyAmount'] = golsCost

                    golsObject = copy.deepcopy(golsTransactionTemplate)
                    transactionsCol.insert_one(golsObject)
