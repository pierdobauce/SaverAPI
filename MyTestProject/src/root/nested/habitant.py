'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.constantes import Constantes

class Habitant(object):
    "Un habitant du monde virtuel"
    vitessemax=0
    vision=0
    positionx=Constantes.nondefini
    positiony=Constantes.nondefini
    nextpositionx=Constantes.nondefini
    nextpositiony=Constantes.nondefini
    terrain=Constantes.nondefini
    forme=Constantes.nondefini
    formemove=Constantes.nondefini
    type=""

    def __init__(self, ter, posx, posy):
        "Constructeur de la classe habitant"
        self.positionx=posx
        self.positiony=posy
        self.terrain=ter
        self.type="Habitant"
        
    def computemove(self):
        "Fonction par défaut si pas instanciée en héritage"
        #print ("This inhabitant as no computemove() method")
        #print(type(self))
        
    def performmove(self):
        "Fonction par défaut si pas instanciée en héritage"
        #print ("This inhabitant as no performmove() method")
        #print(type(self))        
        
    def aftermove(self):
        "Fonction par défaut si pas instanciée en héritage"
        #print ("This inhabitant as no aftermove() method")
        #print(type(self))
                
    def display(self, txtwidget):
        "Fonction par défaut si pas instanciée en héritage"
        #print ("This inhabitant as no display() method")
        #print(type(self))
        
    def disparaitre(self):
        "Fonction par défaut si pas instanciée en héritage"
        #print ("This inhabitant as no disparaitre() method")
        #print(type(self))