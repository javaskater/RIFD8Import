#!/usr/bin/python3
# -*- coding: utf8 -*-

'''
Created on 13 mai 2016

@author: jpmena
'''

import os
import csv
from utils.Log import Log
from domain.Settings import SettingsD8ImportRandosJour
from rest.RandoRestActions import RandoRestAction

class BatchRJ(object):

    def __init__(self, env='dev', log_path=None):
        all_settings=SettingsD8ImportRandosJour()
        self.settings=all_settings.options(env)
        self.champs_date=self.settings['getCrsfTokenRestAction']['url']
        self.log_object=Log(log_path)
        self.rractions=RandoRestAction(self.settings, self.log_object)
    
    
    def importRandosJour(self):
        path_csv = os.path.join(self.settings['pathCsvs'],self.settings['ficCsvRandosCreer']['file'])
        if os.path.exists(path_csv):
            #first we get a token using a simple GET MEthod !!!
            self.rractions.getTokenAndHeaders()
            csvfile = open(path_csv, "r", encoding='utf-8')
            reader = csv.reader(csvfile)
            indice=0
            indice_traite_ok=0
            for csv_row in reader:
                if indice > 0:
                    self.log_object.p("+ on traite la ligne {0}".format(indice))
                    self.rractions.createHike(csv_row)
                indice += 1
            self.log_object.p("sur {0} lignes traitees, {1} effectivement inserees".format(indice, indice_traite_ok))
        else:
            self.log_object.p("ERREUR: le fichier {0} est inconnu, Abandon !!!".format(path_csv))


if __name__ == '__main__':
    brj = BatchRJ(env='dev',log_path="erreurs.log")
    brj.importRandosJour()