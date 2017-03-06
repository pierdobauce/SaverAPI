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
    "Ecriture d'une entrée de sauvegarde"
    isjson=request.is_json
    print("is_json:", isjson)
    jsonstring=request.get_json(force=True, silent=True)
    jsonstring=jsonstring.replace("'",'"')
    print("json:", jsonstring)
    parsedjson = json.loads(jsonstring)
    entryid=datetime.datetime.now()
    parsedjson["entryid"]="cobaye_"+entryid.strftime("%Y-%m-%d_%H:%M:%S_%f")
    stockage.append(parsedjson)
    obj1=deepcopy(parsedjson)
    del obj1["start"]
    del obj1["tours"]
    stockagelight.append(obj1)
    data = {
        "status":"OK",
        "entry":str(entryid)
    }
    returnjs = json.dumps(data)

    resp = Response(returnjs, status=200, mimetype='application/json')
    return resp

@app.route('/serverAPI', methods = ['GET'])
def api_get():
    "Lecture d'un résumé de toutes les entrée de sauvegarde"
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
    "Lecture d'une entrée sépcifique de sauvegarde"
    returnstr="vide"
    for majorkey in stockage:
        print ("Clé de niveau 0: ", majorkey['entryid'])
        if majorkey['entryid']==entryid:
            returnstr=majorkey
            break

    data = {
        "status":"OK",
        "entry": returnstr
    }
    returnjs = json.dumps(data)

    resp = Response(returnjs, status=200, mimetype='application/json')
    return resp

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
