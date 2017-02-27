'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.terrain import Terrain
from tkinter import *
from random import randrange
import requests

class Simulateur(object):
    "le simulateur faisant tourner le monde virtuel"
    terrain=0
    cptmove=0
    newnour=0

    def __init__(self, dicoparam, visible=1):
        "Constructeur de la classe Simulateur"
        terrainlg=dicoparam['largeur']
        terrainht=dicoparam["hauteur"]
        nbcob=dicoparam['nb cobayes']
        nbpred=dicoparam['nb prédateurs']
        nbnour=dicoparam['nb nourritures']
        self.newnour=dicoparam['nb tours réapparition nourriture']
        self.terrain=Terrain(terrainlg, terrainht, visible)  # Création de l'aire de jeu
        self.cptmove=0
        self.terrain.stockagestr=self.terrain.stockagestr+"'tours':["
        for i in range(nbcob):
            self.terrain.ajouthabitant("Cobaye", randrange(self.terrain.dimensionx-10+5) , randrange(self.terrain.dimensiony-10+5))
        for i in range(nbpred):
            self.terrain.ajouthabitant("Predateur", randrange(self.terrain.dimensionx-10+5) , randrange(self.terrain.dimensiony-10+5))
        for i in range(nbnour):
            self.terrain.ajouthabitant("NourritureFixe", randrange(self.terrain.dimensionx-10+5) , randrange(self.terrain.dimensiony-10+5))
        self.terrain.stocker(self.cptmove, first=1)


    def computemove(self):
        "Calcul des mouvements à venir de tous les habitants du terrain"
        self.terrain.computemove()
        
    def performmove(self):
        "Réalisation des mouvements calculés de tous les habitants du terrain"
        self.terrain.performmove()        
        
    def aftermove(self):
        "Réalisation des actions post mouvements de tous les habitants du terrain"
        self.terrain.aftermove()
        self.cptmove=self.cptmove+1
        if (self.cptmove%self.newnour == 0):
            self.terrain.ajouthabitant("NourritureFixe", randrange(self.terrain.dimensionx-10+5) , randrange(self.terrain.dimensiony-10+5))
        self.terrain.stocker(self.cptmove)
        
    def display(self, txtwidget):
        "Donner à chaque objet (habitant, mais pas que...) l'opportunité d'afficher quelque chose sur le controleur"
        txtwidget.delete(1.0, END)
        txtwidget.insert(END, "Compteur de mouvement: {}.\n".format(self.cptmove))
        self.terrain.display(txtwidget)
        if (self.terrain.gameover==True):
            if (self.terrain.visible==1):
                self.terrain.fenterrain.destroy()
            thesurvie=self.cptmove
            if (thesurvie>999):
                thesurvie=999
            self.terrain.stockagestr=self.terrain.stockagestr+"],'end':{{'survie':{0}}}}}".format(thesurvie)
            print("stockagestr:", self.terrain.stockagestr)
            #jsonaenvoyer='{"Survie":'+str(random.randrange(1,1000))+',"Trace":"longue chaine d etapes"}'
            r=requests.post('http://127.0.0.1:5000/serverAPI', json=self.terrain.stockagestr)
            print("status code:", r.status_code)
            print("response:", r.text)

        
    def isgameover(self):
        "Détermine si la partie est terminée"
        return self.terrain.isgameover(self.cptmove)