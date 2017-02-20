'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.terrain import Terrain
from tkinter import *
from random import randrange

class Simulateur(object):
    "le simulateur faisant tourner le monde virtuel"
    terrain=0
    cptmove=0
    newnour=0

    def __init__(self, dicoparam):
        "Constructeur de la classe Simulateur"
        terrainlg=dicoparam['largeur']
        terrainht=dicoparam["hauteur"]
        nbcob=dicoparam['nb cobayes']
        nbpred=dicoparam['nb prédateurs']
        nbnour=dicoparam['nb nourritures']
        self.newnour=dicoparam['nb tours réapparition nourriture']
        self.terrain=Terrain(terrainlg, terrainht)  # Création de l'aire de jeu
        self.cptmove=0
        self.terrain.stockagestr=self.terrain.stockagestr+"'tours':["
        #self.terrain.stockagestr=self.terrain.stockagestr+"'tours':[{{'tour nb':{0},".format(self.cptmove)
        #self.terrain.stockagestr=self.terrain.stockagestr+"'population':["
        #print("stockagestr:", self.terrain.stockagestr)
        # Ajout des habitants
        for i in range(nbcob):
            self.terrain.ajouthabitant("Cobaye", randrange(self.terrain.dimensionx-10+5) , randrange(self.terrain.dimensiony-10+5))
        for i in range(nbpred):
            self.terrain.ajouthabitant("Predateur", randrange(self.terrain.dimensionx-10+5) , randrange(self.terrain.dimensiony-10+5))
        for i in range(nbnour):
            self.terrain.ajouthabitant("NourritureFixe", randrange(self.terrain.dimensionx-10+5) , randrange(self.terrain.dimensiony-10+5))
        self.terrain.stocker(self.cptmove, first=1)
        #self.terrain.stockagestr=self.terrain.stockagestr+"]}"
        #print("stockagestr:", self.terrain.stockagestr)


    def computemove(self):
        "Calcul des mouvements à venir de tous les habitants du terrain"
        self.terrain.computemove()
        
    def performmove(self):
        "Réalisation des mouvements calculés de tous les habitants du terrain"
        self.terrain.stockage.append(["Simulation Nbmove", self.cptmove])
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
            self.terrain.fenterrain.destroy()
            self.terrain.stockagestr=self.terrain.stockagestr+"],'end':{{'survie':{0}}}}}".format(self.cptmove)
            print("stockagestr:", self.terrain.stockagestr)
        
    def isgameover(self):
        "Détermine si la partie est terminée"
        return self.terrain.isgameover(self.cptmove)