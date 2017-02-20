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

@app.route('/serverAPI', methods = ['POST'])
def api_post():
    isjson=request.is_json
    print("is_json:", isjson)
    jsonstring=request.get_json(force=True, silent=True)
    print("json:", jsonstring)
    parsedjson = json.loads(jsonstring)
    print("La survie a été de: ", parsedjson["Survie"])
    print("La séquence: ", parsedjson["Trace"])
    entryid=datetime.datetime.now()
    parsedjson["EntryId"]="Cobaye "+str(entryid)
    stockage.append(parsedjson)
    data = {
        "Status":"OK",
        "Entry":str(entryid)
    }
   # data["Entry"]='"'+str(entryid)+'"'
    returnjs = json.dumps(data)

    resp = Response(returnjs, status=200, mimetype='application/json')
    return resp

@app.route('/serverAPI', methods = ['GET'])
def api_get():
    data = {"Status":"OK"}
    data["Taille"]=len(stockage)
    cpteur=1
    for obj in stockage:
        obj1=deepcopy(obj)
        del obj1["Trace"]
        data[cpteur]=obj1
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
