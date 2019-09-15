from flask import Flask
from flask import request
from bson import json_util
from datetime import datetime, timedelta
import pymongo
import geopy.distance
import json
import math
app = Flask(__name__)

applicationClient = pymongo.MongoClient('mongodb://localhost:27017/')
applicationDb = applicationClient['budgetBuddy']
transactionsCol = applicationDb['transactions']
customersCol = applicationDb['customers']

@app.route('/merchantDetails', methods = ['POST'])
def merchantDetails():
    if not request.content_type == 'application/json':
        return ''
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    merchantName = data['merchantName']
    dayRange = data['dayRange']
    customerAgeLower = data['customerAgeLower']
    customerAgeUpper = data['customerAgeUpper']
    customerGender = data['customerGender']

    kilometresPerLatitudeDegree = 111.09
    latitudeInRadians = latitude * (math.pi / 180)
    kilometresPerLongitudeDegree = math.cos(latitudeInRadians) * kilometresPerLatitudeDegree

    # 1km
    deltaDegreeLat = (1 / kilometresPerLatitudeDegree)
    deltaDegreeLong = (1 / kilometresPerLongitudeDegree)

    pastDate = datetime.today() - timedelta(days=dayRange)
    pastDate = pastDate.strftime("%Y-%m-%d")

    localTransactions = transactionsCol.find({
        'locationLatitude': {
            '$gt': latitude - deltaDegreeLat,
            '$lt': latitude + deltaDegreeLat
        },
        'locationLongitude': {
            '$gt': longitude - deltaDegreeLong,
            '$lt': longitude + deltaDegreeLong
        },
        'merchantName': merchantName,
        'originationDateTime': {
            '$gt': pastDate
        }
    })

    retVal = {}
    transaction = localTransactions[0]
    transactionDict = json.loads(json.dumps(transaction, default=json_util.default))
    coords1 = (latitude, longitude)
    coords2 = (transactionDict['locationLatitude'], transactionDict['locationLongitude'])
    retVal['distance'] = geopy.distance.vincenty(coords1, coords2).km * 1000
    retVal['city'] = transaction['locationCity']
    retVal['address'] = transaction['locationStreet']

    retVal['spendingDistribution'] = {}
    count = 0
    totalSpending = 0
    purchases = []
    for transaction in localTransactions:
        transactionDict = json.loads(json.dumps(transaction, default=json_util.default))

        customerId = transactionDict['customerId']
        customer = customersCol.find_one({'id': customerId})
        customer = json.loads(json.dumps(customer, default=json_util.default))
        if customer['age'] >= customerAgeLower and customer['age'] <= customerAgeUpper and customer['gender'] == customerGender:
            count += 1
            totalSpending += transactionDict['currencyAmount']
            purchases.append(transactionDict['currencyAmount'])

            distributionKey = str(int(round(transactionDict['currencyAmount'])))
            if not distributionKey in retVal['spendingDistribution'].keys():
                retVal['spendingDistribution'][distributionKey] = 0
            retVal['spendingDistribution'][distributionKey] += 1

    purchases.sort()
    if count > 0:
        retVal['averageSpending'] = totalSpending / count
        retVal['medianSpending'] = purchases[int(count/2)] if count % 2 == 1 else \
            (purchases[int(count/2)] + purchases[int(count/2) - 1]) / 2
        retVal['transactionCount'] = count

    return retVal

@app.route('/localTransactions', methods = ['POST'])
def localTransactions():
    if not request.content_type == 'application/json':
        return ''
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    dayRange = data['dayRange']

    kilometresPerLatitudeDegree = 111.09
    latitudeInRadians = latitude * (math.pi / 180)
    kilometresPerLongitudeDegree = math.cos(latitudeInRadians) * kilometresPerLatitudeDegree

    # 1km
    deltaDegreeLat = (1 / kilometresPerLatitudeDegree)
    deltaDegreeLong = (1 / kilometresPerLongitudeDegree)

    pastDate = datetime.today() - timedelta(days=dayRange)
    pastDate = pastDate.strftime("%Y-%m-%d")

    localTransactions = transactionsCol.find({
        'locationLatitude': {
            '$gt': latitude - deltaDegreeLat,
            '$lt': latitude + deltaDegreeLat
        },
        'locationLongitude': {
            '$gt': longitude - deltaDegreeLong,
            '$lt': longitude + deltaDegreeLong
        },
        'originationDateTime': {
            '$gt': pastDate
        }
    })

    merchantDict = {}
    coords1 = (latitude, longitude)
    for transaction in localTransactions:
        transactionDict = json.loads(json.dumps(transaction, default=json_util.default))
        if not transactionDict['merchantName'] in merchantDict.keys():
            coords2 = (transactionDict['locationLatitude'], transactionDict['locationLongitude'])
            merchantDict[transactionDict['merchantName']] = {
                'distance': geopy.distance.vincenty(coords1, coords2).km * 1000,
                'totalSpending': 0,
                'count': 0,
            }
        merchantDict[transactionDict['merchantName']]['totalSpending'] += transactionDict['currencyAmount']
        merchantDict[transactionDict['merchantName']]['count'] += 1

    retVal = { 'merchants': [] }
    for (merchantName, merchantInfo) in  merchantDict.items():
        retVal['merchants'].append({
            'name': merchantName,
            'distance': merchantInfo['distance'],
            'averageSpending': merchantInfo['totalSpending'] / merchantInfo['count']
        })

    return retVal

if __name__ == '__main__':
    app.run()
