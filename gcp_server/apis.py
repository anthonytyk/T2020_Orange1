import requests

def getUserDetails(customerID):
    httpstring = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/"+ str(customerID) + "/details"
    r = requests.get(httpstring, headers={"token":"aa9a045b-4279-4d49-b099-d322a2eaecac", "identity": "Group10"})
    return r.json()

def getTransactions(customerID):
    accID = accountID(customerID)
    httpstring = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/" + str(accID) + "?from=01-01-2018&to=01-10-2019"
    r = requests.get(httpstring, headers={"token":"aa9a045b-4279-4d49-b099-d322a2eaecac", "identity": "Group10"})
    return r.json()

def getMonthlyExpenditure(customerID, year, month):
    accID = accountID(customerID)
    httpstring = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/" + str(accID) + "?from="+ str(month) + "-01-" + str(year) + "&to=01-30-2019"
    r = requests.get(httpstring, headers={"token":"aa9a045b-4279-4d49-b099-d322a2eaecac", "identity": "Group10"})
    expenditure = 0
    for i in r.json():
        expenditure += float(i["amount"])
    return expenditure

def getMonthlyTransactions(customerID, year, month):
    accID = accountID(customerID)
    httpstring = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/" + str(accID) + "?from="+ str(month) + "-01-" + str(year) + "&to="+ str(month)+ "-28-"  + str(year) 
    print(httpstring)

    r = requests.get(httpstring, headers={"token":"aa9a045b-4279-4d49-b099-d322a2eaecac", "identity": "Group10"})  
    print(r)
    return r.json()

def accountID(customerID):
    httpstring = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/" + str(customerID)
    r = requests.get(httpstring, headers={"token":"aa9a045b-4279-4d49-b099-d322a2eaecac", "identity": "Group10"})
    return r.json()[0]['accountId']

def getMonthlyTransactionsBreakDown(customerID, year, month):
    accID = accountID(customerID)
    httpstring = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/" + str(accID) + "?from="+ str(month) + "-01-" + str(year) + "&to="+ str(month)+ "-28-"  + str(year) 
    r = requests.get(httpstring, headers={"token":"aa9a045b-4279-4d49-b099-d322a2eaecac", "identity": "Group10"}) 

    breakdown = {"F&B":0, "TRANSPORT":0, "ATM":0, "TRANSFER":0}
    for i in r.json():
        print(i)
        if i['type'] == "DEBIT":
            breakdown[i['tag']] += float(i['amount'])
    return breakdown

