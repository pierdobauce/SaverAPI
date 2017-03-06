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
    progresslabel=Constantes.nondefini
    stockage={}
    timetic=0
    progresstext="0/999"

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

        self.progress = ttk.Progressbar(self.fenreplay, orient="horizontal", length=self.dimensionx-100, mode="determinate")
        self.progress["value"] = 0
        self.progress["maximum"] = self.stockage["entry"]["end"]["survie"]
        self.progresstext="0/{0}".format(self.progress["maximum"])
        self.progresslabel=Label(self.fenreplay, text= self.progresstext)
        self.progresslabel.grid(row=1, column=0, sticky=E)
        self.boutonmoins = Button(self.fenreplay, text = '<', command = self.clickmoins, repeatdelay=500, repeatinterval=100).grid(row=1, column=1)

        self.boutonpluss = Button(self.fenreplay, text = '>', command = self.clickplus,  repeatdelay=500, repeatinterval=100).grid(row=1, column=3)
        self.progress.grid(row=1, column=2)
        
        self.canvas = Canvas(self.fenreplay,bg='dark grey',height=self.dimensiony,width=self.dimensionx)
        self.canvas.grid(row=2, columnspan=4, sticky=S)
        
    def clickmoins(self):
        "Clic sur le bouton moins-un-tick"
        if (self.timetic>0):
            self.timetic=self.timetic-1
            self.progresstext="{0}/{1}".format(self.timetic,self.progress["maximum"])
            self.progresslabel["text"]=self.progresstext
        self.progress["value"]=self.timetic
        self.afficher(5)
        
    def clickplus(self):
        "Clic sur le bouton plus-un-tick"
        if (self.timetic<self.progress["maximum"]):
            self.timetic=self.timetic+1
            self.progresstext="{0}/{1}".format(self.timetic,self.progress["maximum"])
            self.progresslabel["text"]=self.progresstext
        self.progress["value"]=self.timetic
        self.afficher(8)
        
        
    def afficher(self, tic):
        "Effacer le canvas et construire la configuration du tick"
        self.canvas.delete("all")
        posx=100
        posy=100
        forme = self.canvas.create_oval(posx-5 , posy-5, posx+5, posy+5, width=2, fill='red')
        print("replay:", self.stockage["entry"]["tours"][tic]["population"])
        