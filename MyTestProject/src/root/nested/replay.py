'''
Created on 5 mars 2017

@author: OPBO6311
'''

from root.nested.constantes import Constantes
from copy import deepcopy
import requests
from tkinter import ttk
from tkinter import *
import json

class Replay(object):
    "La fenêtre permettant de rejouer une partie spécifique"
    dimensionx=400
    dimensiony=400
    fenreplay=Constantes.nondefini
    canvas=Constantes.nondefini
    boutonmoins=Constantes.nondefini
    boutonplus=Constantes.nondefini
    progress=Constantes.nondefini
    stockage={}

    def __init__(self, entryid):
        "Constructeur de la classe permettant de rejouer une partie spécifique"
        
        #Aller chercher le json avec lequel on va jouer. Le stocker.
        target='http://127.0.0.1:5000/serverAPI/{0}'.format(entryid)
        r=requests.get(target)
        print("status code:", r.status_code)
        print("response:", r.text)
        parsedjson = json.loads(r.text)
        self.stockage=deepcopy(parsedjson)
        print("replay ", self.stockage)
        self.dimensionx=self.stockage["entry"]["start"]["dimensions"]["x"]
        self.dimensiony=self.stockage["entry"]["start"]["dimensions"]["y"]
      
        #Créer la fenêtre et l'afficher.
        self.fenreplay=Tk()
        self.fenreplay.title("Replay pour {0}".format(self.stockage["entry"]["entryid"]))

        self.boutonmoins = Button(self.fenreplay, text = '<', command = self.clickmoins).grid(row=1, column=0)
        self.progress = ttk.Progressbar(self.fenreplay, orient="horizontal", length=self.dimensionx-100, mode="determinate")
        self.progress.grid(row=1, column=1)
        self.progress["value"] = 0
        self.progress["maximum"] = self.stockage["entry"]["end"]["survie"]
        self.boutonpluss = Button(self.fenreplay, text = '>', command = self.clickplus).grid(row=1, column=2)
        
        self.canvas = Canvas(self.fenreplay,bg='dark grey',height=self.dimensiony,width=self.dimensionx)
        self.canvas.grid(row=2, columnspan=3, sticky=S)
        
    def clickmoins(self):
        print("Click moins")
        
    def clickplus(self):
        print("Click plus")
        
        