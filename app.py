import code
from dataclasses import dataclass
from distutils.log import debug
from email import message
from lib2to3.pgen2 import token
from os import stat
import re
import secrets
import string
from sys import setswitchinterval
from tabnanny import check
from unittest.result import failfast
from urllib import response
import uuid
from django.template import Origin
from sqlalchemy import false, true
from flask import Flask, abort, jsonify, make_response, request
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from functools import wraps
from bson.objectid import ObjectId



app = Flask(__name__)
CORS(app, resources = {r"/*":{"orgins":"*"}}) #What??
bcrypt = Bcrypt(app) #what?

mongo = MongoClient('localhost',27017)
db = mongo['backendtask'] # db name

app.config['JWT_SECRET_KEY'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.Rf32AQPl_46JhmGqlJ7aBldhtqjnDJ3zdMj0rPINi_8"




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")
            
            print(token[1]) # mock
            
        if not token[1] or token[0] != "Bearer":
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token[1], app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            print(data)
            
            if data is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        return f(*args, **kwargs)

    print(decorated)
    return decorated
       
@app.route('/login', methods=["POST"])
def login():
    message = ""
    resp_data = {}
    code = 500
    status = "fail"  
       
    try:
        data = request.get_json()
        #user = db['users'].find_one({"username": f'{data["username"]}'}) 
        user = db["user"].find_one({"username":data["username"]})
        if user: 
            user['_id'] = str(user['_id'])
            
            if user and bcrypt.check_password_hash(user['password'], data['password']):
                time = datetime.utcnow() + timedelta(hours=24)
                token = jwt.encode({
                    "user" : {
                        "username" : f"{user['username']}",
                        "id" : f"{user['_id']}"
                    },
                    "exp" : time
                }, app.config['JWT_SECRET_KEY'])

                del user['password']
                
                message = f"user authenticated"
                code = 200
                status = "successfully"
                resp_data['token'] = token.encode().decode('utf-8')
                resp_data['user'] = user
        
            else:
                message = f"wrong password"
                code = 401
                status = "fail"
                
        else:
            message = f"mock 1 2 3 "
            code = 401
            status = "fail"
    
    except Exception as ex:
            message = f"{ex}"
            code = 500
            status = "fail"
    
    return jsonify({'status': status, "data": resp_data, "message": message}), code
            
@app.route('/signup', methods=["POST"])  
def save_user():
    message = ""
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        #TODO kontrol ekle daha önce kayıt olmuş mu?
        
        data['_id'] = str(uuid.uuid4())
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8') #if password is not encp, its not stored in db
        data['created'] = datetime.now()
        data['admin'] = 1

        resp = db["user"].insert_one(data)
        
        if resp.acknowledged: #wth??
            status = "success"
            message = "user created"
            code = 201 
            
    except Exception as ex:
        message = f"{ex}"
        status = "fail"
        code = 500
    return jsonify({'status': status, "message": message}), code
  
@app.route('/user', methods=["POST", "GET"])
def createUser():
    res = []
    code = 500
    status = "fail"
    message = ""
    
    try:
        if(request.method == 'POST'):
            data = request.get_json()
            user = db["user"].find_one({"username":data["username"]})
            if(user): 
                res = db['user'].insert_one(request.get_json())
                if res.acknowledged:
                    status = "success"
                    message = "user created"
                    code = 201
                    res = {"_id": f"{res.inserted_id}"}
                else:
                    message = "user not created - insert error"
                    code = 500
                    status = "fail" 
            else:
                message = "opsss!! You are not Admin"
                code = 500
                status = "fail" 
                
        else:
            for i in db['user'].find().sort("_id", -1):
                i['_id'] = str(i['_id'])
                res.append(i)
            if res:
                message = "users retrieved"
                status = "success"
                code = 200
            else:
                message = "no users found"
                status = "success"
                code = 200
    except Exception as ex:
        res = {"error": f"{ex}"}
        
    return jsonify({'status': status, "data": res, "message": message}), code

@app.route('/user/<id>', methods=["GET"])
@token_required
def get_by_id(id):
    res = []
    code = 500
    message = ""
    status = "fail"
    try:
        user = db['user'].find_one({'_id': str(id)})
        user['_id'] = str(user['_id']) # id is jsonserializable
             
        if user is None:
            message = "User not found"
            code = 401
            status = "fail"
            
        else:
            message = "User found :)"
            code = 200
            status = "susccess"
            return jsonify({'User' : user, 'status': status, "message": message}), code
            
    except Exception as ex:
        res = {"error": f"{ex}"}
        
    return jsonify({'status': status, "message": message, "data": res}), code    
    
@app.route('/user/<id>', methods=["DELETE"])
@token_required
def delete_one(id):
    data = {}
    code = 500
    message = ""
    status ="fail"
    
    try:
        if(request.method == 'DELETE'):
            response = db['user'].delete_one({'_id': str(id)})
            if response:
                message = "User deleted successfully"
                code = 201
                status = "success"
            else:
                message = "delete failed"
                code = 404
                status = "fail"
        else:
            message = "Method of Delete is failed"
            status = "fail"
            code = 500
    except Exception as ex:
        message = f"{ex}"
        status = "ERROR"

    return  jsonify({'status': status, "message": message, "data": data}), code

@app.route('/user/<id>', methods=["PUT","GET"])
@token_required
def update_one(id):
    user = {}
    message = ""
    status ="fail"
    code = 500
    try:
        if(request.method == 'PUT'):
            response = db['user'].update_one({'_id': str(id)}, {'$set': request.get_json()})
            if response:
                message = "User updated successfully"
                status = "success"
                code = 200
            else:
                message = "update unsuccessful"
                status = "fail"
                code = 404
        else:
            user = db['user'].find_one({'_id': str(id)})
            user['_id'] = str(user['_id'])
            if user:
                message = "User found"
                status = "success"
                code = 201
            else:
                message = "User not found- failed"
                status = "fail"
                code  = 404
    except Exception as ex:
        message = f"{ex}"
        status = "ERROR"
    return jsonify({'status': status, "message": message, "data": user}), code
    
@app.route('/weather', methods=["GET"])
def weather_info():
    res = []
    code = 500
    message = ""
    status = "fail"
    
    summary = request.args.get('Summary')
    visibility = request.args.get('Visibility')
    condition = request.args.get('PrecipType')
    date = request.args.get('Date')
    temprature  = request.args.get('Temperature')
    speed = request.args.get('Wind Speed')
    pressure = request.args.get('Pressure')
    
    try:
        if visibility:
            for i in  db['weatherHistory'].find({'Visibility (km)': float(visibility)}).sort("_id", -1):
                i['_id'] = str(i['_id'])
                res.append(i)
        elif summary:
            for i in  db['weatherHistory'].find({'Summary': summary}).sort("_id", -1):
                i['_id'] = str(i['_id'])
                res.append(i)
        elif condition:
            for i in db['weatherHistory'].find({'Precip Type': condition}).sort("_id", -1):
                i['_id'] = str(i['_id'])
                res.append(i)
        elif date:
            for i in db['weatherHistory'].find({'Formatted Date': date}).sort("_id", -1):
                i['_id'] = str(i['_id'])
                res.append(i)
        elif temprature:
            for i in db['weatherHistory'].find({'Apparent Temperature (C)': temprature}).sort("_id", -1):
                i['_id'] = str(i['_id'])
                res.append(i)
        elif speed:
            for i in  db['weatherHistory'].find({'Wind Speed (km/h)': float(speed)}).sort("_id", -1):
                i['_id'] = str(i['_id'])
                res.append(i)
        elif pressure:
            for i in  db['weatherHistory'].find({'Pressure (millibars': float(pressure)}).sort("_id", -1):
                i['_id'] = str(i['_id'])
                res.append(i)
        else:
            code = 404
            message = "No data found for this weather feature"
            status = "fail"
            return jsonify({'status': status, "message": message, "data": res}), code
        
        code = 200
        message = "Weather info retrieved"
        status = "success"

    except Exception as ex:
        res = {"error": f"{ex}"}
        
    return jsonify({'message': message, 'status': status, 'data': res }), code



@app.route('/')
def test():
    return "amanda aman oldu mu şimdii", 200

if __name__ == "__main__":
    app.run(debug = true)
    




    