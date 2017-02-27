'''
Created on 30 nov. 2016

@author: opbo6311
'''
from root.nested.cobaye import Cobaye
from root.nested.predateur import Predateur
from tkinter import *
from root.nested.nourriturefixe import Nourriturefixe
from root.nested.constantes import Constantes
from math import sqrt

class Terrain(object):
    "Le terrain virtuel dans lequel les cobayes, prédateurs et nourritures se trouvent, et vivent"
    dimensionx=400
    dimensiony=400
    population=[]
    fenterrain=Constantes.nondefini
    canvas=Constantes.nondefini
    gameover=False
    stockagestr=""
    visible=1

    def __init__(self, dimx, dimy, visible):
        "Constructeur de la classe Terrain"
        del self.population[:]
        self.stockagestr=""
        self.dimensionx=dimx
        self.dimensiony=dimy
        self.visible=visible
        if (visible==1):
            self.fenterrain=Tk()
            self.fenterrain.title("Simulation")
            self.canvas = Canvas(self.fenterrain,bg='dark grey',height=self.dimensiony,width=self.dimensionx)
            self.canvas.pack(side=LEFT)
        self.gameover=False
        self.stockagestr="{{'start':{{'dimensions':{{'x':{0},'y':{1}}}}},".format(dimx, dimy)
        print("stockagestr:", self.stockagestr)
             
    def ajouthabitant(self, ltype, posx, posy):
        "Ajout d'un habitant à une certaine position"    
        if (ltype == "Cobaye"):
            hab=Cobaye(self, posx, posy)
            self.population.append(hab)
        elif (ltype=="Predateur"):
            hab=Predateur(self, posx, posy)
            self.population.append(hab)
        elif (ltype=="NourritureFixe"):
            hab=Nourriturefixe(self, posx, posy)
            self.population.append(hab)

    def retirerhabitant(self, habitantaretirer):
        "Retirer un habitant du terrain"
        habitantaretirer.disparaitre()
        self.population.remove(habitantaretirer)
        if (habitantaretirer.type=="Cobaye"):
            self.gameover=True   
        del habitantaretirer 
        #print("Habitant retiré du terrain")

    def trouverhabitant(self, type, posx, posy):
        "Retourne le pointeur vers l'habitant le plus proche de la position donnée, avec le type donné"    
        lhabitant=Constantes.nondefini
        distance=Constantes.infini
        
        for hab in self.population:
            if hab.type==type:
                dist=sqrt((hab.positionx-posx)**2+(hab.positiony-posy)**2)
                if dist<distance:
                    distance=dist
                    lhabitant=hab
        
        return lhabitant

    def computemove(self):
        "Calcul des mouvements de tous les habitants"
        for hab in self.population:
            hab.computemove()
            
    def performmove(self):
        "Réalisation des mouvements de tous les habitants"
        for hab in self.population:
            hab.performmove()
            
    def aftermove(self):
        "Réalisation des actions post-mouvements de tous les habitants"
        for hab in self.population:
            hab.aftermove()
    
    def display(self, txtwidget):
        "Donner à chaque objet (habitant, mais pas que...) l'opportunité d'afficher quelque chose sur le controleur"
        for hab in self.population:
            hab.display(txtwidget)
        #print(self.stockage)
        if (self.visible)==1:
            self.canvas.update_idletasks()

    def stocker(self, cptmove, first=0):
        "Stockage dans je json"
        if (first==0):
             self.stockagestr=self.stockagestr+","
        self.stockagestr=self.stockagestr+"{{'tour nb':{0},".format(cptmove)
        self.stockagestr=self.stockagestr+"'population':["
        first=1
        for hab in self.population:
            if (first==1):
                first=0
                hab.stocker(first=1)
            else:    
                hab.stocker()
        self.stockagestr=self.stockagestr+"]}"
        #print("stockagestr:", self.stockagestr)
        
    def plusprocheselontype(self, posx, posy, type):
        "Retourne les coordonnées de l'habitant de type donné le plus proche d'une position donnée"
        retposx=Constantes.nondefini
        retposy=Constantes.nondefini
        distance=Constantes.infini
        
        for hab in self.population:
            if hab.type==type:
                dist=sqrt((hab.positionx-posx)**2+(hab.positiony-posy)**2)
                if dist<distance:
                    distance=dist
                    retposx=hab.positionx
                    retposy=hab.positiony
        
        return retposx, retposy
    
    def isgameover(self, cptmove):
        "Détermine si la partie est terminée"
        #print("gameover: ", self.gameover)
        return self.gameover
    