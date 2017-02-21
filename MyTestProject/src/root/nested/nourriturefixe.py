'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.nourriture import Nourriture
from root.nested.habitant import Habitant

class Nourriturefixe(Nourriture):
    "De la nourriture fixe pour le cobaye dans le monde virtuel"


    def __init__(self, ter, posx, posy):
        "Constructeur de la classe Nourriturefixe"
        super().__init__(ter, posx, posy)
        self.vitessemax=0
        self.forme = self.terrain.canvas.create_rectangle(self.positionx-5 , self.positiony-5, self.positionx+5, self.positiony+5, width=2, fill='green')
        self.type="NourritureFixe"

    def aftermove(self):
        "Réalisation des actions post move"
        # Si on est consommé, sortir du plateau.
        
    def disparaitre(self):
        "Actions à réaliser avant de faire sortir cet habitant"
        self.terrain.canvas.delete(self.forme)

    def stocker(self, first=0):
        "Stockage dans je json"
        if (first==0):
            self.terrain.stockagestr=self.terrain.stockagestr+","
        self.terrain.stockagestr=self.terrain.stockagestr+"{{'catégorie':'nourriturefixe','x':{0},'y':{1}}}".format(self.positionx, self.positiony)
