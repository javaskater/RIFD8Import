#!/usr/bin/python3
# -*- coding: utf8 -*-

'''
Created on 24 mars 2016

@author: jpmena
'''

import datetime

from batch.Curl import Curl
from utils.authentication import Authentication

from utils.Log import Log



#from collections import OrderedDict
class RandoRestAction(object):
    def __init__(self, settings, log_objet):
        self.mon_curl=Curl()
        self.log_objet=log_objet
        self.settings=settings
        self.authentication=Authentication('adminD8Rif','php39Rando57')
        self.token=None
        self.d8_post_headers=None
        self.d8_post_data=None
    
    def getTokenAndHeaders(self):
        self.token=self.moncurl.secureRequest(self.settings['getCrsfTokenRestAction']['url'], paramsRetry={'timeout':3,'nbRetries':5})
        self.d8_post_headers={'Accept':'application/hal+json',
                     'Content-Type':'application/hal+json',
                     'X-CSRF-Token':self.token.decode('ascii'),
                     'Authorization':self.authentication.createBasicAuthorizationHeader()}    
    
    def createHike(self,csv_row,champs_date):
        self.d8_post_headers={"_links":{"type":{self.settings['creerRandoRestAction']['posttype_url']},
                                      "uid":[{"target_id":"1","url":"\/fr\/user\/1"}]}
        date_randonnee =  datetime.datetime.strptime(csv_row[self.settings['ficCsvRandosCreer']['date_rif']], '%Y-%m-%d').date()
        for champs in self.settings['ficCsvRandosCreer']['mapping']:
            d8_name=champs[0]
            d8_type=champs[2]
            csv_pos=champs[1]
            self.log_objet.p("++ le champs drupal {0} de type {1} a pour rang {2} et valeur: {3}".format(d8_name, d8_type, csv_pos, csv_row[csv_pos]))
            self.d8_post_data[d8_name] = [{"value":self.translate(d8_type,csv_row[csv_pos],date_randonnee)}]
        #hal_json_d8_postdata = json.dumps(d8_postdata)
        hal_json_d8_postdata = self.d8_post_data
        #hal_json_d8_postdata = {"uid": [{"url": "\\/fr\\/user\\/1", "target_id": "1"}], "_links": {"type": {"href": "http://dru8rif.ovh/rest/type/node/randonnee_de_journee"}}, "body": [{"value": "Le Faubourg Poissonni\u00e8re dans toute sa diversit\u00e9, les Petites Ecuries, quelques passages du quartier Strasbourg, l'h\u00f4pital St Louis, la place Ste Marthe."}], "title": [{"value": "Promenade dans le 10\u00e8me"}], "field_date": [{"value": "2016-02-01"}], "field_gare_depart": [{"value": ""}], "field_heure_depar": [{"value": "2016-02-01T00:00:00"}], "field_gare_depart_retour": [{"value": "m\u00e9tro Belleville"}], "field_heure_arrivee_aller": [{"value": "2016-02-01T17:00:00"}]}
        self.log_objet.p("je veux inserer le contenu |{0}|".format(hal_json_d8_postdata))
        self.log_objet.p("avec pour Headers |{0}|".format(self.d8_post_headers))
        try:
            d8_insertion=self.mon_curl.secureRequest(self.settings['creerRandoRestAction']['post_url'], method='POST',
                reqparams=hal_json_d8_postdata,headers=self.d8_post_headers,paramsRetry={'timeout':3,'nbRetries':3})
        except:
            self.error_report("impossible d'inserer le contenu |{0}|".format(hal_json_d8_postdata))
    
    def translate(self, type, csv_value, date_randonnee):
        if type == 'rifdate':
            return date_randonnee.strftime("%Y-%m-%d")
        elif type == 'riftime':
            datetime_horaire = datetime.datetime.strptime(csv_value, '%Y/%m/%d %H:%M:%S').time()
            return "{0}T{1}".format(date_randonnee.strftime("%Y-%m-%d"),datetime_horaire.strftime("%H:%M:%S"))
        else:
            return csv_value
        
    
if __name__ == '__main__':
    pass