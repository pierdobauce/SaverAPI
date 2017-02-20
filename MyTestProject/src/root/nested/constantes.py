'''
Created on 12 déc. 2016

@author: opbo6311
'''

class Constantes(object):
    "Les constantes pour tout l'environnement"
    infini=99999999
    nondefini=-1
    cobayeenergiedepart=100
    coutenergiecobayepartour=1
    energienourriturefixe=50
    dimensionresultx=750
    dimensionresulty=100

    def __init__(self):
        "Constructeur de la classe des constantes"
      
      
""" Exemple de format de message
{
    "start":{
        "dimensions": { "x": 300, "y": 600}
    },
    "tours": [
        { 
            "tour nb": 0,
            "population":[
              {"catégorie":"cobaye", "x": 305, "y": 700, "energie": 45},
              {"catégorie":"predateur", "x": 301, "y": 600},
              {"catégorie":"predateur", "x": 302, "y": 600},
              {"catégorie":"predateur", "x": 303, "y": 600},
              {"catégorie":"nourriturefixe", "x": 303, "y": 600}
              ]
        },
        { 
            "tour nb": 1,
            "population":[
              {"catégorie":"cobaye", "x": 305, "y": 700, "energie": 45},
              {"catégorie":"predateur", "x": 301, "y": 600},
              {"catégorie":"predateur", "x": 302, "y": 600},
              {"catégorie":"predateur", "x": 303, "y": 600},
              {"catégorie":"nourriturefixe", "x": 303, "y": 600}
              ]
         }
    ],
    "end":{
        "survie": 100
    }
}
"""