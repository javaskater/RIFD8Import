#!/usr/bin/python3
# -*- coding: utf8 -*-

'''
Created on 24 mars 2016

@author: jpmena
'''
from batch.Curl import Curl
from utils.authentication import Authentication
from utils.Log import Log
from domain.Settings import SettingsD8ImportRandosJour

import os
import csv
import datetime
#from collections import OrderedDict


class RandoRestAction(object):
    def __init__(self, env='dev', error_log=None, trace_log=None):
        all_settings = SettingsD8ImportRandosJour()
        self.settings = all_settings.options(env)
        self.trace_log = trace_log
        self.error_log = error_log
        
    def trace(self,msg):
        if self.trace_log is not None:
             self.trace_log.p(msg)
        print(msg)
            
    def error_report(self,msg):
        error_msg = "ERREUR: {0}!!!!".format(msg)
        if self.error_log is not None:
             self.error_log.p(error_msg)
        print(error_msg)
    
    def translate(self, type, csv_value, date_randonnee):
        if type == 'rifdate':
            return date_randonnee.strftime("%Y-%m-%d")
        elif type == 'riftime':
            datetime_horaire = datetime.datetime.strptime(csv_value,'%Y/%m/%d %H:%M:%S').time()
            return "{0}T{1}".format(date_randonnee.strftime("%Y-%m-%d"),datetime_horaire.strftime("%H:%M:%S"))
        else:
            return csv_value
        
    def importRandosJour(self):
        path_csv = os.path.join(self.settings['pathCsvs'],self.settings['ficCsvRandosCreer']['file'])
        champs_date = self.settings['ficCsvRandosCreer']['date_rando']
        if os.path.exists(path_csv):
            moncurl=Curl()
            #first we get a token using a simple GET MEthod !!!
            token=moncurl.secureRequest('http://dru8rif.ovh/rest/session/token', paramsRetry={'timeout':3,'nbRetries':5})
            a=Authentication('adminD8Rif','php39Rando57')
            d8_post_headers={'Accept':'application/hal+json',
                     'Content-Type':'application/hal+json',
                     'X-CSRF-Token':token.decode('ascii'),
                     'Authorization':a.createBasicAuthorizationHeader()}
            csvfile = open(path_csv, "r", encoding='utf-8')
            reader = csv.reader(csvfile)
            indice=0
            indice_traite_ok=0
            for row in reader:
                if indice > 0:
                    self.trace("+ on traite la ligne {0}".format(indice))
                    d8_postdata={"_links":{"type":{"href":"http://dru8rif.ovh/rest/type/node/randonnee_de_journee"}},
                                      "uid":[{"target_id":"1","url":"\/fr\/user\/1"}]}
                    date_randonnee =  datetime.datetime.strptime(row[champs_date], '%Y-%m-%d').date()
                    for champs in self.settings['ficCsvRandosCreer']['mapping']:
                        d8_name=champs[0]
                        d8_type=champs[2]
                        csv_pos=champs[1]
                        self.trace("++ le champs drupal {0} de type {1} a pour rang {2} et valeur: {3}".format(d8_name, d8_type, csv_pos, row[csv_pos]))
                        d8_postdata[d8_name] = [{"value":self.translate(d8_type,row[csv_pos],date_randonnee)}]
                    #hal_json_d8_postdata = json.dumps(d8_postdata)
                    hal_json_d8_postdata = d8_postdata
                    #hal_json_d8_postdata = {"uid": [{"url": "\\/fr\\/user\\/1", "target_id": "1"}], "_links": {"type": {"href": "http://dru8rif.ovh/rest/type/node/randonnee_de_journee"}}, "body": [{"value": "Le Faubourg Poissonni\u00e8re dans toute sa diversit\u00e9, les Petites Ecuries, quelques passages du quartier Strasbourg, l'h\u00f4pital St Louis, la place Ste Marthe."}], "title": [{"value": "Promenade dans le 10\u00e8me"}], "field_date": [{"value": "2016-02-01"}], "field_gare_depart": [{"value": ""}], "field_heure_depar": [{"value": "2016-02-01T00:00:00"}], "field_gare_depart_retour": [{"value": "m\u00e9tro Belleville"}], "field_heure_arrivee_aller": [{"value": "2016-02-01T17:00:00"}]}
                    self.trace("je veux inserer le contenu |{0}|".format(hal_json_d8_postdata))
                    self.trace("avec pour Headers |{0}|".format(d8_post_headers))
                    try:
                        d8_insertion=moncurl.secureRequest('http://dru8rif.ovh/entity/node?_format=hal_json', method='POST',
                            reqparams=hal_json_d8_postdata,headers=d8_post_headers,
                            paramsRetry={'timeout':3,'nbRetries':3})
                        indice_traite_ok += 1
                    except:
                        self.error_report("impossible d'inserer le contenu |{0}|".format(hal_json_d8_postdata))
                indice += 1
            self.trace("sur {0} lignes traitees, {1} effectivement inserees".format(indice, indice_traite_ok))
        else:
            self.trace("ERREUR: le fichier {0} est inconnu, Abandon !!!".format(path_csv))

if __name__ == '__main__':
    rra = RandoRestAction(error_log=Log("erreurs.log"),trace_log=Log("trace.log"))
    rra.importRandosJour()