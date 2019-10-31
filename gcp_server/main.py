from flask import Flask, jsonify
from flask import request
from flask import abort
from apis import getTransactions, getMonthlyExpenditure, getUserDetails, getMonthlyTransactions, getMonthlyTransactionsBreakDown
import hashlib, binascii, os 
from flask_cors import CORS

app = Flask(__name__)

db = {}
users = {}
users["limzeyang"] = {"name": "Ze Yang", "password": "123321", "customerID": 1}
users["marytan"] = {"name": "Hui Shan", "password": "321123", "customerID": 2}
users["prasannaghali"] = {"name": "Prasanna", "password": "12345678", "customerID": 3}

userHashs = {}

def getHash(t):
    hash_object = hashlib.sha1(t.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig[:8]

@app.route('/user', methods=['GET'])
def getUser():
    if not request.headers:
        abort(400)
    if not request.headers['token']:
        abort(400)
    if request.headers['token'] not in userHashs:
        print("HEREEEE")
        print(request.headers['token'])
        return "no such user", 300
    user = userHashs[request.headers['token']]

    return jsonify(getUserDetails(user["customerID"])), 200

@app.route('/transactions', methods=['POST'])
def getTransactionsAPI():
    if not request.headers:
        abort(400)
    year = request.json['year']
    month = request.json['month']
    customerID = request.json['id']
    t = getMonthlyTransactions(customerID, year, month)
    return jsonify(t), 200

@app.route('/monthlybreakdown', methods=['POST'])
def apibreakdown():
    if not request.headers:
        abort(400)
    
    year = request.json['year']
    month = request.json['month']
    customerID = request.json['id']
    t = getMonthlyTransactionsBreakDown(customerID, year, month)
    return jsonify(t), 200


@app.route('/monthlyexpenditure', methods=['GET'])
def getMonthlyExpenditureAPI():
    if not request.headers:
        abort(400)
    if not request.headers['token']:
        abort(400)
    if request.headers['token'] not in userHashs:
        return "no such user", 300

    user = userHashs[request.headers['token']]
    year = request.json['year']
    month = request.json['month']
    t = getMonthlyExpenditure(user["customerID"], year, month)
    return jsonify(t), 200


@app.route('/login', methods=['POST'])
def login():
    if not request.json:
        abort(400)
    username = request.json["user"]
    password = request.json["password"]
    
    if username not in users:
        print("No such user")
        return "No such user", 300
    if password != users[username]["password"]:
        print("Wrong password")
        return "Wrong password", 300
    print("User logged in!")
    print("Password: " + password)
    print("User:" + username)
    userHashs[str(getHash(username+password))] = users[username]
    return jsonify({"hash": getHash(str(username)+str(password)), "user": users[username]}), 201


if __name__ == '__main__':
    app.run(debug=True)
    CORS(app)
