'''
Created on 4 déc. 2016

@author: opbo6311
'''
from tkinter import *
from root.nested.simulateur import Simulateur
from root.nested.constantes import Constantes
from root.nested.replay import Replay
import time
import requests
import random
import json
import gc
from colour import Color
from root.nested.RepeatedTimer import RepeatedTimer
from copy import deepcopy

if __name__ == '__main__':

    def serialrun():
        global sim
        serialtournb=int(vnbserialrun.get())
        for tournb in range(0,serialtournb):
            startsimulation(0)
            while (sim.isgameover()==False):
                sim.computemove()
                sim.performmove()
                sim.aftermove()
                sim.display(txtwidget)
                cansummary.update_idletasks()
                #    fenctrl.after(50, automove)
                #    fenctrl.after(10000, automove)
                #time.sleep(0.1)
            txtwidget.insert(END, "La cobaye est mort")
            del sim
            gc.collect()

    def startsimulation(visible=1):
        "Démarrage de la simulation"
        global sim
        print("Démarrage de la simulation")
        dicoparam={}
        largeur=int(vlg.get())
        dicoparam['largeur']=largeur
        hauteur=int(vht.get())
        dicoparam['hauteur']=hauteur
        nbcob=int(vnbcob.get())
        dicoparam['nb cobayes']=nbcob
        nbpred=int(vnbpred.get())
        dicoparam['nb prédateurs']=nbpred
        nbnour=int(vnbnour.get())
        dicoparam['nb nourritures']=nbnour
        newnour=int(vnewnour.get())
        dicoparam['nb tours réapparition nourriture']=newnour
        sim=Simulateur(dicoparam, visible)
    
    def computemove():
        "Calculs nécessaires pour les mouvements sur le terrain"
        sim.computemove()

    def performmove():
        "Réalisation des mouvements"
        sim.performmove()

    def aftermove():
        "Réalisation des actions post mouvements"
        sim.aftermove()
        sim.display(txtwidget)

    def automove():
        "Automatisation du compute puis move en boucle"
        while (sim.isgameover()==False):
            sim.computemove()
            sim.performmove()
            sim.aftermove()
            sim.display(txtwidget)
            #    fenctrl.after(50, automove)
            #    fenctrl.after(10000, automove)
            time.sleep(0.1)
        txtwidget.insert(END, "La cobaye est mort")
        
    def apitestpost():
        "Test d'un POST vers l'API server"
        for i in range(0,5):
            jsonaenvoyer='{"end":{"survie":'+str(random.randrange(1,1000))+'},"tours":1}'
            r=requests.post('http://127.0.0.1:5000/serverAPI', json=jsonaenvoyer)
            print("status code:", r.status_code)
            print("response:", r.text)
            #time.sleep(0.0001)
    
    def apitestget():
        "Test d'un GET vers l'API server"
        global cansummarylastentrynb, stockage
        r=requests.get('http://127.0.0.1:5000/serverAPI')
        #print("status code:", r.status_code)
        #print("response:", r.text)
        parsedjson = json.loads(r.text)
        stockage=deepcopy(parsedjson)
        taille=parsedjson["taille"]
        cansummary.delete("all")
        cansummary.update_idletasks()
        cansummarylastentrynb=0
        for i in range(1,taille+1):
            survie=parsedjson[str(i)]["end"]["survie"]
            addsummaryentry(survie)

    def apitestgetentry():
        "Test d'un GET(entry) vers l'API server"
        for i in range(0,5000): 
            addsummaryentry(random.randrange(0,999))
   
    def addsummaryentry(value):
        "Ajout d'une entrée dans le canvas d'affichage des résultats"
        # value entre 0 et 999.
        global cansummarylastentrynb, colors
        posentryx=10*(cansummarylastentrynb % (Constantes.dimensionresultx/10))
        posentryy=10*(cansummarylastentrynb // (Constantes.dimensionresultx/10))
        cansummary.create_rectangle(posentryx,posentryy,posentryx+9,posentryy+9,fill=colors[value])
        cansummarylastentrynb=cansummarylastentrynb+1
   
    def clicdroitcansummary(event):
        global cansummarymenu, stockage, entryidtostart
        print ("Clic droit en ", event.x % 10, event.y // 10)
        nbentry=int((event.x // 10)+1 +(Constantes.dimensionresultx/10)*(event.y // 10))
        nbentrystr="{0:d}".format(nbentry)
        survie=stockage[nbentrystr]["end"]["survie"]
        #print ("survie: ", survie)
        entryidtostart=stockage[nbentrystr]["entryid"]
        menutext="Survie: {0}".format(survie)
        cansummarymenu.entryconfig(1, label=menutext)
        cansummarymenu.post(event.x_root, event.y_root)

    def clicreleasedroitcansummary(event):
        print ("Clic release droit en ", event.x, event.y)

    def cansummarystartwindow():
        global fenreplay
        print("Start window for: ", entryidtostart)
        fenreplay=Replay(entryidtostart)
   
    fenctrl=Tk()
    fenctrl.title("Controleur")
    
    txtlg = Label(fenctrl, text ='Terrain de simulation, largeur :').grid(row=1, sticky=E)
    vlg = StringVar(fenctrl, value='600')
    entrylg = Entry(fenctrl, textvariable=vlg).grid(row=1, column=1)
    txtht = Label(fenctrl, text ='Terrain de simulation, hauteur :').grid(row=1, column=2, sticky=E)
    vht = StringVar(fenctrl, value='300')
    entryht = Entry(fenctrl, textvariable=vht).grid(row=1, column=3)
    txtnbcob = Label(fenctrl, text ='Terrain de simulation, nb de cobayes :').grid(row=2, sticky=E)
    vnbcob = StringVar(fenctrl, value='1')
    entrynbcob = Entry(fenctrl, textvariable=vnbcob).grid(row=2, column=1)
    txtnbpred = Label(fenctrl, text ='Terrain de simulation, nb de prédateurs :').grid(row=2, column=2, sticky=E)
    vnbpred = StringVar(fenctrl, value='6')
    entrynbpred = Entry(fenctrl, textvariable=vnbpred).grid(row=2, column=3)
    txtnbnour = Label(fenctrl, text ='Terrain de simulation, nb de nourritures au départ :').grid(row=3, sticky=E)
    vnbnour = StringVar(fenctrl, value='4')
    entrynbnour = Entry(fenctrl, textvariable=vnbnour).grid(row=3, column=1)
    txtnewnour = Label(fenctrl, text ='Terrain de simulation, nb de tours pour faire réapparaitre la nourriture :').grid(row=3, column=2, sticky=E)
    vnewnour = StringVar(fenctrl, value='65')
    entrynewnour = Entry(fenctrl, textvariable=vnewnour).grid(row=3, column=3)
    txtnbtour = Label(fenctrl, text ='Terrain de simulation, nb de tours maximum :').grid(row=4, sticky=E)
    vnbtour = StringVar(fenctrl, value='1000')
    entrynbtour = Entry(fenctrl, textvariable=vnbtour).grid(row=4, column=1)
    txtnbserialrun = Label(fenctrl, text ='Terrain de simulation, nb de tours par serial run :').grid(row=4, column=2, sticky=E)
    vnbserialrun = StringVar(fenctrl, value='10')
    entrynbserialrun = Entry(fenctrl, textvariable=vnbserialrun).grid(row=4, column=3)

    bstartsim = Button(fenctrl, text='Start simulation', command=startsimulation).grid(row=8, column=0, sticky=E)
    bcompmove = Button(fenctrl, text='Compute move', command=computemove).grid(row=8, column=1)
    bmove = Button(fenctrl, text='Move', command=performmove).grid(row=8, column=2)
    baftermove = Button(fenctrl, text='After Move', command=aftermove).grid(row=8, column=3)
    bauto = Button(fenctrl, text='Auto move', command=automove).grid(row=8, column=4)
    bserialrun = Button(fenctrl, text='Serial Run', command=serialrun).grid(row=8, column=5)
    
    txtwidget= Text(fenctrl, height=10, width=80)
    txtwidget.grid(row=9, columnspan=6, sticky=W)

    btestAPIpost = Button(fenctrl, text='API test (POST)', command=apitestpost).grid(row=10, column=0, sticky=W)
    btestAPIget = Button(fenctrl, text='API test (GET)', command=apitestget).grid(row=10, column=1)
    btestAPIgetentry = Button(fenctrl, text='API test (Get entry)', command=apitestgetentry).grid(row=10, column=2)

    cansummary= Canvas(fenctrl, width =Constantes.dimensionresultx, height =Constantes.dimensionresulty, bg ='white', scrollregion=(0,0,Constantes.dimensionresultx,1000))
    cansummary.grid(row=11, columnspan=6, sticky=W)
    cansummary.bind("<Button-3>", clicdroitcansummary)
    cansummary.bind("<ButtonRelease-3>", clicreleasedroitcansummary)
    cansummarylastentrynb=0
    red = Color("red")
    colors = list(red.range_to(Color("green"),1000))
    vbar=Scrollbar(fenctrl,orient=VERTICAL)
    vbar.grid(row=11, column=5, sticky='ns')
    vbar.config(command=cansummary.yview)
    cansummary.config(width =Constantes.dimensionresultx, height =Constantes.dimensionresulty)
    cansummary.config(yscrollcommand=vbar.set)
    
    cansummarymenu = Menu(fenctrl, tearoff=0)
    cansummarymenu.add_command(label="Test", command=cansummarystartwindow)
    
    rt = RepeatedTimer(2, apitestget) # it auto-starts, no need of rt.start()
    
    stockage={}
    entryidtostart=""
    fenreplay=Constantes.nondefini
    
    fenctrl.mainloop()