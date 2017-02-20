'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.habitant import Habitant

class Nourriture(Habitant):
    "De la nourriture pour le cobaye dans le monde virtuel"


    def __init__(self, ter, posx, posy):
        "Constructeur de la classe Nourriture"
        super().__init__(ter, posx, posy)
        self.type="Nourriture"