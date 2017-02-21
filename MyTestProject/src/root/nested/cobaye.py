'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.habitant import Habitant
from tkinter import *
from root.nested.terrain import *
from root.nested.constantes import Constantes
from math import sqrt

class Cobaye(Habitant):
    "Un cobaye dans le monde virtuel"
    nivenergie=Constantes.cobayeenergiedepart
    distancenourriture=Constantes.infini

    def __init__(self, ter, posx, posy):
        "Constructeur de la classe Cobaye"
        super().__init__(ter, posx, posy)
        self.vitessemax=10
        self.vision=40
        self.forme = self.terrain.canvas.create_oval(self.positionx-5 , self.positiony-5, self.positionx+5, self.positiony+5, width=2, fill='blue')
        self.type="Cobaye"
        self.nivenergie=Constantes.cobayeenergiedepart

    def computemove(self):
        "Calcul du prochain mouvement de ce cobaye"
        # Trouver les prédateurs à proximité. Choisir le plus proche. Le fuir.
        predposx, predposy = self.terrain.plusprocheselontype(self.positionx, self.positiony, "Predateur")
        #print ("positions retournées move fuite cobaye", predposx, predposy)
        vecteurdepx=0
        vecteurdepy=0
        self.nextpositionx=Constantes.nondefini
        self.nextpositiony=Constantes.nondefini
        if (predposx != Constantes.nondefini):
            vecteurdepx=self.positionx-predposx
            vecteurdepy=self.positiony-predposy
            #print ("vecteurdep brut move fuite cobaye", vecteurdepx, vecteurdepy)
            # Normalisation par rapport à la vitessemax
            normevecteurdep=sqrt((vecteurdepx)**2 + (vecteurdepy)**2)
            if normevecteurdep <= self.vision:
                vecteurdepx=self.vitessemax*vecteurdepx/normevecteurdep
                vecteurdepy=self.vitessemax*vecteurdepy/normevecteurdep
                #print ("vecteurdep normalisé move fuite cobaye", vecteurdepx, vecteurdepy)
                self.nextpositionx=self.positionx+vecteurdepx
                if (self.nextpositionx<7):
                    self.nextpositionx=7
                if (self.nextpositionx>self.terrain.dimensionx-7):
                    self.nextpositionx=self.terrain.dimensionx-7
                self.nextpositiony=self.positiony+vecteurdepy
                if (self.nextpositiony<7):
                    self.nextpositiony=7
                if (self.nextpositiony>self.terrain.dimensiony-7):
                    self.nextpositiony=self.terrain.dimensiony-7
                # Affichage du vecteur
                self.formemove=self.terrain.canvas.create_line(self.positionx, self.positiony, self.nextpositionx, self.nextpositiony, arrow="last", width=2, fill='blue')
        if (self.nextpositionx == Constantes.nondefini):
            # Si la faim tiraille, il faut chercher à manger.
            nourposx, nourposy = self.terrain.plusprocheselontype(self.positionx, self.positiony, "NourritureFixe")
            #print ("positions retournées move nourriture cobaye", nourposx, nourposy)
            if (nourposx != Constantes.nondefini):
                # Aller dans la direction en question
                vecteurdepx=self.positionx-nourposx
                vecteurdepy=self.positiony-nourposy
                #print ("vecteurdep brut move nourriture cobaye", vecteurdepx, vecteurdepy)
                # Normalisation par rapport à la vitessemax
                normevecteurdep=sqrt((vecteurdepx)**2 + (vecteurdepy)**2)
                if normevecteurdep <= 20*self.vision:
                    if normevecteurdep>self.vitessemax:
                        vecteurdepx=-self.vitessemax*vecteurdepx/normevecteurdep
                        vecteurdepy=-self.vitessemax*vecteurdepy/normevecteurdep
                    else:
                        vecteurdepx=-vecteurdepx
                        vecteurdepy=-vecteurdepy
                    #print ("vecteurdep normalisé move nourriture cobaye", vecteurdepx, vecteurdepy)
                    self.nextpositionx=self.positionx+vecteurdepx
                    self.nextpositiony=self.positiony+vecteurdepy
                    # Affichage du vecteur
                    self.formemove=self.terrain.canvas.create_line(self.positionx, self.positiony, self.nextpositionx, self.nextpositiony, arrow="last", width=2, fill='blue')
            #else:
                # Se déplacer au hasard

    def performmove(self):
        "Réalisation du move déjà calculé"
        # Le tour de mouvement coute de la nourriture
        self.nivenergie=self.nivenergie-Constantes.coutenergiecobayepartour
        # Tester si mouvement nécessaire
        if self.nextpositionx != Constantes.nondefini:
            # Effacer la flèche.
            self.terrain.canvas.delete(self.formemove)
            self.formemove=Constantes.nondefini
            # Bouger le cobaye.
            self.positionx=self.nextpositionx
            self.positiony=self.nextpositiony
            self.nextpositionx=Constantes.nondefini
            self.nextpositiony=Constantes.nondefini
            self.terrain.canvas.coords(self.forme, self.positionx-5, self.positiony-5, self.positionx+5, self.positiony+5)

    def aftermove(self):
        "Réalisation des actions post move"
        # Si la nourriture est atteinte, recharger le compteur de nourriture, et dire à la nourriture qu'elle est consommée.
        # Savoir si une nourriture est au contact. 
        nourposx, nourposy = self.terrain.plusprocheselontype(self.positionx, self.positiony, "NourritureFixe")
        #print ("positions retournées after move nourriture cobaye", nourposx, nourposy)
        if (nourposx != Constantes.nondefini):
            # mesurer la distance
            vecteurx=self.positionx-nourposx
            vecteury=self.positiony-nourposy
            #print ("vecteurdep brut after move nourriture cobaye", vecteurx, vecteury)
            # Calcul de la distance
            self.distancenourriture=sqrt((vecteurx)**2 + (vecteury)**2)
            #print("Distance after move nourriture cobaye", distancenourriture)
            if (self.distancenourriture < 0.1):
                self.nivenergie=self.nivenergie+Constantes.energienourriturefixe
                lanourriture=self.terrain.trouverhabitant("NourritureFixe", nourposx, nourposy)
                self.terrain.retirerhabitant(lanourriture)   

        # Si le cobaye n'a plus d'énergie, il meurt.
        if (self.nivenergie == 0):
            self.terrain.retirerhabitant(self)
            print("Le cobaye est mort de faim")
            
        # Si on est mort, sortir du plateau.

    def disparaitre(self):
        "Actions à réaliser avant de faire sortir cet habitant"
        self.terrain.canvas.delete(self.forme)

    def display(self, txtwidget):
        "Donner à chaque objet (habitant, mais pas que...) l'opportunité d'afficher quelque chose sur le controleur"
        txtwidget.insert(END, "Cobaye: distance à la nourriture: {}.\n".format(self.distancenourriture))
        txtwidget.insert(END, "Cobaye: niveau d'énergie: {}.\n ".format(self.nivenergie))

    def stocker(self, first=0):
        "Stockage dans je json"
        self.terrain.stockagestr=self.terrain.stockagestr+"{{'catégorie':'cobaye','x':{0},'y':{1},'energie':{2}}}".format(self.positionx, self.positiony, self.nivenergie)
