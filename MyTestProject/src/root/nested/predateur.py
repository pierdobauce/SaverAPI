'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.habitant import Habitant
from root.nested.constantes import Constantes
from math import sqrt

class Predateur(Habitant):
    "Un prédateur dans le monde virtuel" 

    def __init__(self, ter, posx, posy):
        "Constructeur de la classe Predateur"
        super().__init__(ter, posx, posy)
        self.vitessemax=8
        self.vision=35
        self.forme = self.terrain.canvas.create_oval(self.positionx-5 , self.positiony-5, self.positionx+5, self.positiony+5, width=2, fill='red')
        self.terrain.stockage.append(["Prédateur Start", self.positionx, self.positiony ])
        self.type="Predateur"
        #self.terrain.stockagestr=self.terrain.stockagestr+",{{'catégorie':'prédateur','x':{0},'y':{1}}}".format(self.positionx, self.positiony)
        #print("stockagestr:", self.terrain.stockagestr)

    def computemove(self):
        "Calcul du prochain mouvement de ce prédateur"
        # Trouver les cobayes à proximité. Choisir le plus proche. Le traquer.
        cobposx, cobposy = self.terrain.plusprocheselontype(self.positionx, self.positiony, "Cobaye")
        #print ("positions retournées move prédateur", cobposx, cobposy)
        vecteurdepx=0
        vecteurdepy=0
        self.nextpositionx=Constantes.nondefini
        self.nextpositiony=Constantes.nondefini
        if (cobposx != Constantes.nondefini):
            vecteurdepx=self.positionx-cobposx
            vecteurdepy=self.positiony-cobposy
            #print ("vecteurdep brut move prédateur", vecteurdepx, vecteurdepy)
            # Normalisation par rapport à la vitessemax
            normevecteurdep=sqrt((vecteurdepx)**2 + (vecteurdepy)**2)
            if normevecteurdep <= self.vision:
                vecteurdepx=-self.vitessemax*vecteurdepx/normevecteurdep
                vecteurdepy=-self.vitessemax*vecteurdepy/normevecteurdep
                #print ("vecteurdep normalisé move prédateur", vecteurdepx, vecteurdepy)
                self.nextpositionx=self.positionx+vecteurdepx
                self.nextpositiony=self.positiony+vecteurdepy
                # Affichage du vecteur
                self.formemove=self.terrain.canvas.create_line(self.positionx, self.positiony, self.nextpositionx, self.nextpositiony, arrow="last", width=2, fill='red')

    def performmove(self):
        "Réalisation du move déjà calculé"
        # Tester si mouvement nécessaire
        if self.nextpositionx != Constantes.nondefini:
            # Effacer la flèche.
            self.terrain.canvas.delete(self.formemove)
            self.formemove=Constantes.nondefini
            # Bouger le predateur.
            self.positionx=self.nextpositionx
            self.positiony=self.nextpositiony
            self.nextpositionx=Constantes.nondefini
            self.nextpositiony=Constantes.nondefini
            self.terrain.canvas.coords(self.forme, self.positionx-5, self.positiony-5, self.positionx+5, self.positiony+5)
            self.terrain.stockage.append(["Prédateur Move", self.positionx, self.positiony])

    def aftermove(self):
        "Réalisation des actions post move"
        # Si un cobaye est atteint, alors le tuer.
        
    def stocker(self, first=0):
        "Stockage dans je json"
        if (first==0):
            self.terrain.stockagestr=self.terrain.stockagestr+","
        self.terrain.stockagestr=self.terrain.stockagestr+"{{'catégorie':'prédateur','x':{0},'y':{1}}}".format(self.positionx, self.positiony)
