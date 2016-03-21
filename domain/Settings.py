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
        self.parametres_prod={'pathCsvs':u'/home/jpmena/RIF/transfert_rifrandoextra_03-07-2016/importations',
                         'paramsProxy':None,
                          #'paramsProxy':{'host':'dgproxy.appli.dgi','port':8080},#pour le bureau où l'on est derrière un proxy
                         'paramsRetry':{'timeout':60,'nbRetries':5},
                         'getCrsfTokenRestAction':{'url':'http://dru8rif.ovh/rest/session/token','method':'GET'},
                         'restUser':{'name':'adminD8Rif','password':'php39Rando57'},
                         'outputDir':u'D:/Applis/batchAnimateurs/out',
                         'mail':{'email':u'adminadh@rifrando.fr','serveurSMTP':u'smtp.numericable.fr'}
                         }
        self.parametres_dev={'pathCsvs':u'/home/jpmena/RIF/transfert_rifrandoextra_03-07-2016/importations',
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
        self.parametres_prod.update({ # D8 field versus Python field in the csv file  (0 starting rang)...
                         'ficCsvRandosCreer':{'file' : 'randonnees.csv', 'mapping':[{'body':{23:'string'}},{'title':{4:'string'}},{'field_date':{1:['rifdate','{0:%Y-%m-%d}']}},
                                                                                    {'field_gare_depart':{23:'string'}},{'field_heure_depar':{11:['riftime','{0:%Y-%m-%dT%H:%M:%S}']}},
                                                                                    {'field_gare_depart_retour':{23:'string'}},{'field_heure_arrivee_aller':{15:['riftime','{0:%Y-%m-%dT%H:%M:%S}']}}]},
                         'creerRandoRestAction':{'url':'http://dru8rif.ovh/rest/type/node','method':'POST','node':'randonnee_de_journee'},
                         })
        self.parametres_prod.update({ # D8 field versus Python field in the csv file  (0 starting rang)...
                         'ficCsvRandosCreer':{'file' : 'randonnees.csv', 'mapping':[{'body':{23:'string'}},{'title':{4:'string'}},{'field_date':{1:['rifdate','{0:%Y-%m-%d}']}},
                                                                                    {'field_gare_depart':{23:'string'}},{'field_heure_depar':{11:['riftime','{0:%Y-%m-%dT%H:%M:%S}']}},
                                                                                    {'field_gare_depart_retour':{23:'string'}},{'field_heure_arrivee_aller':{15:['riftime','{0:%Y-%m-%dT%H:%M:%S}']}}]},
                         'creerRandoRestAction':{'url':'http://dru8rif.ovh/rest/type/node','method':'POST','node':'randonnee_de_journee'},
                         })

if __name__ == '__main__':
    pass
