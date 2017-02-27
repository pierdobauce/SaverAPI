'''
Created on 16 janv. 2017

@author: opbo6311
'''

from flask import Flask, url_for, request, Response
import json
import datetime
from copy import deepcopy

app = Flask(__name__)
stockage=[]
stockagelight=[]

@app.route('/serverAPI', methods = ['POST'])
def api_post():
    isjson=request.is_json
    print("is_json:", isjson)
    jsonstring=request.get_json(force=True, silent=True)
    jsonstring=jsonstring.replace("'",'"')
    print("json:", jsonstring)
    parsedjson = json.loads(jsonstring)
    entryid=datetime.datetime.now()
    parsedjson["entryid"]="cobaye "+str(entryid)
    stockage.append(parsedjson)
    obj1=deepcopy(parsedjson)
    del obj1["start"]
    del obj1["tours"]
    stockagelight.append(obj1)
    data = {
        "status":"OK",
        "entry":str(entryid)
    }
   # data["Entry"]='"'+str(entryid)+'"'
    returnjs = json.dumps(data)

    resp = Response(returnjs, status=200, mimetype='application/json')
    return resp

@app.route('/serverAPI', methods = ['GET'])
def api_get():
    data = {"status":"OK"}
    data["taille"]=len(stockage)
    cpteur=1
    for obj in stockagelight:
        data[cpteur]=obj
        cpteur=cpteur+1
    returnjs=json.dumps(data)
    resp = Response(returnjs, status=200, mimetype='application/json')
    return resp


@app.route('/serverAPI/<entryid>', methods = ['GET'])
def api_getentry(entryid):
    return 'You are reading ' + entryid

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid


if __name__ == '__main__':
    app.run()
