'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.nourriture import Nourriture

class Nourriturestatique(Nourriture):
    "De la nourriture statique pour le cobaye"

    def __init__(self):
        "Constructeur de la classe Nourriturestatique"
        self.vitessemax=0
        self.type="Nourriturestatique"