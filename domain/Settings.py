# -*- coding: utf-8 -*-
'''
Created on 21 mars. 2016

@author: jpmena
'''
class Settings(object):
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        self.parametres_prod=None
        self.parametres_dev=None
    
    def getParamsDev(self):
        return self.parametres_dev
    
    def getParamsProd(self):
        return self.parametres_prod
    
    def options(self,environment='prod'):
        if environment == 'dev':
            return self.getParamsDev()
        else:
            return self.getParamsProd()

class SettingsD8Import(Settings):
    def __init__(self, *args, **kwargs):
        Settings.__init__(self,*args, **kwargs)
        self.parametres_gen_prod={'pathCsvs':u'/home/jpmena/RIF/transfert_rifrandoextra_03-07-2016/importations',
                         'paramsProxy':None,
                          #'paramsProxy':{'host':'dgproxy.appli.dgi','port':8080},#pour le bureau où l'on est derrière un proxy
                         'paramsRetry':{'timeout':60,'nbRetries':5},
                         'getCrsfTokenRestAction':{'url':'http://dru8rif.ovh/rest/session/token','method':'GET'},
                         'restUser':{'name':'adminD8Rif','password':'php39Rando57'},
                         'outputDir':u'D:/Applis/batchAnimateurs/out',
                         'mail':{'email':u'adminadh@rifrando.fr','serveurSMTP':u'smtp.numericable.fr'}
                         }
        self.parametres_gen_dev={'pathCsvs':u'/home/jpmena/RIF/transfert_rifrandoextra_03-07-2016/importations',
                         'paramsProxy':None,
                          #'paramsProxy':{'host':'dgproxy.appli.dgi','port':8080},#pour le bureau où l'on est derrière un proxy
                         'paramsRetry':{'timeout':60,'nbRetries':5},
                         'getCrsfTokenRestAction':{'url':'http://dru8rif.ovh/rest/session/token','method':'GET'},
                         'restUser':{'name':'adminD8Rif','password':'php39Rando57'},
                         'outputDir':u'D:/Applis/batchAnimateurs/out',
                         'mail':{'email':u'adminadh@rifrando.fr','serveurSMTP':u'smtp.numericable.fr'}
                         }
        

class SettingsD8ImportRandosJour(SettingsD8Import):
    def __init__(self, *args, **kwargs):
        SettingsD8Import.__init__(self,*args, **kwargs)
        self.rjsettings = { # D8 field versus Python field in the csv file  (0 starting rang)...
            'ficCsvRandosCreer':{'file' : 'randonnees.csv', 'date_rando':1 ,'mapping':[['body',22,'string'],['title',4,'string'],['field_date',1,'rifdate'],
                                                                       ['field_gare_depart',19,'string'],['field_heure_depar',11,'riftime'],
                                                                        ['field_gare_depart_retour',23,'string'],['field_heure_arrivee_aller',15,'riftime']],
            'creerRandoRestAction':{'url':'http://pub.rifrando.asso.fr/rest/type/node','method':'POST','node':'randonnee_de_journee'},
        }}
        self.parametres_prod = self.parametres_gen_prod.copy()
        self.parametres_prod.update(self.rjsettings)
        self.parametres_dev = self.parametres_gen_dev.copy() 
        self.parametres_dev.update(self.rjsettings)

if __name__ == '__main__':
    pass
