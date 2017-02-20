'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.nourriture import Nourriture

class Nourritureproie(Nourriture):
    "Nourriture mobile dans le monde virtuel, donc une proie à chasser pour le cobaye"


    def __init__(self):
        "Constructeur de la classe Nourritureproie"
        self.vitessemax=6
        self.type="Nourritureproie"