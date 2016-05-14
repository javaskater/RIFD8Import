#!/usr/bin/python3
# -*- coding: utf8 -*-

'''
Created on 24 mars 2016

@author: jpmena
'''

import datetime
import json
from collections import OrderedDict

from rest.Curl import Curl
from utils.authentication import Authentication
import json

from utils.Log import Log

class RandoRestAction(object):
    def __init__(self, settings, log_objet):
        self.mon_curl=Curl(f_log=log_objet)
        self.log_objet=log_objet
        self.settings=settings
        self.authentication=Authentication('adminD8Rif','php39Rando57')
        self.token=None
        self.d8_post_headers=None
        self.d8_post_data=None
    
    def getTokenAndHeaders(self):
        self.token=self.mon_curl.secureRequest(self.settings['getCrsfTokenRestAction']['url'], paramsRetry={'timeout':3,'nbRetries':5})
        self.d8_post_headers={'Accept':'application/hal+json',
                     'Content-Type':'application/hal+json',
                     'X-CSRF-Token':self.token.decode('ascii'),
                     'Authorization':self.authentication.createBasicAuthorizationHeader()}    
    
    def createHike(self,csv_row):
        #je veux que d'abord le links et l'UID !!!!
        self.d8_post_data=OrderedDict([("_links",{"type":{'href':self.settings['creerRandoRestAction']['posttype_url']}}), ("uid",[{"target_id":"1","url":"\/fr\/user\/1"}])])
        champs_date=csv_row[self.settings['ficCsvRandosCreer']['date_rando']]
        date_randonnee=datetime.datetime.strptime(champs_date, '%Y-%m-%d')
        for champs in self.settings['ficCsvRandosCreer']['mapping']:
            myDictToAdd={}
            d8_name=champs[0]
            d8_type=champs[2]
            csv_pos=champs[1]
            post_value=self.translate(d8_type,csv_row[csv_pos],date_randonnee)
            self.log_objet.p("++ le champs drupal {0} de type {1} a pour rang {2} et valeur: {3}".format(d8_name, d8_type, csv_pos, post_value))
            myDictToAdd = OrderedDict([(d8_name,[{"value":post_value}])])
            self.d8_post_data.update(myDictToAdd)
        try:
            d8_insertion=self.mon_curl.secureRequest(self.settings['creerRandoRestAction']['post_url'], method='POST',
                reqparams=self.d8_post_data,headers=self.d8_post_headers,paramsRetry={'timeout':3,'nbRetries':3})
            return "OK"
        except:
            self.log_objet.p("ERREUR!!!!: impossible d'inserer le contenu |0|".format(json.dumps(self.d8_post_data, indent=4)))
            return "KO"
    
    def translate(self, type, csv_value, date_randonnee):
        if type == 'rifdate':
            return date_randonnee.strftime("%Y-%m-%d")
        elif type == 'riftime':
            if not csv_value == "":
                datetime_horaire = datetime.datetime.strptime(csv_value, '%Y/%m/%d %H:%M:%S').time()
                return "{0}T{1}".format(date_randonnee.strftime("%Y-%m-%d"),datetime_horaire.strftime("%H:%M:%S"))
            else:
                return "{0}T00:00:00".format(date_randonnee.strftime("%Y-%m-%d"))
        elif type == 'integer':
            return int(csv_value)
        else:
            if csv_value == "":
                csv_value="xxxx"
            return csv_value
        
    
if __name__ == '__main__':
    pass