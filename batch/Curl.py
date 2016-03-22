# -*- coding: utf8 -*-
'''
Created on 22 marx 2016

@author: jpmena

https://docs.python.org/3.1/howto/urllib2.html 
for a thorough documentation about handling HTTP requests !!!
'''
from utils.authentication import Authentication

from urllib import request, parse, error 
from time import sleep
import json

class Curl(object):
    def __init__(self,f_log=None,proxy_info=None, ):
        self.proxy_support=None
        self.proxy_opener=None
        self.f_log=f_log
        if proxy_info is not None: #see http://stackoverflow.com/questions/22967084/urllib-request-urlretrieve-with-proxy
            self.proxy_support = request.ProxyHandler({"http":"http://%(host)s:%(port)d" % proxy_info})
        else: #http://www.decalage.info/fr/node/17 force it not to use a proxy
            self.proxy_support = request.ProxyHandler({})
        self.proxy_opener = request.build_opener(self.proxy_support)
        request.install_opener(self.proxy_opener)
    
    def trace(self,msg):
        if self.f_log is not None:
             self.f_log.p(msg)
        else:
            print(msg)
    
    #TODO ajouter l'authentification basique !!!
    def getUrlResponseData(self, url, method='GET', requestparams=None, headers={}):
        resp=None
        try:
            #problème récupérer les données en utf-8
            #http://stackoverflow.com/questions/1020892/urllib2-read-to-unicode
            self.trace('Curl: requete de type {0}, pour l\'URL: {1}'.format(method,url))
            querystring=None

            get_post_data = requestparams
            if requestparams is not None and method == 'GET':
                get_post_data = parse.urlencode(requestparams)
            elif requestparams is not None and method == 'POST':
                get_post_data = json.dumps(requestparams).encode('utf8')
            
            httprequest = request.Request(#https://docs.python.org/3.4/library/urllib.request.html#urllib.request.Request
                url,
                data=get_post_data, 
                headers=headers,
                method=method)

            #réponse 11 de http://stackoverflow.com/questions/24226781/changing-user-agent-in-python-3-for-urrlib-urlopen
            connection=request.urlopen(httprequest)
            resp = connection.read()    

            self.trace('Curl: les données {0} de {1} ont été correctement récupérées'.format(repr(resp), url))
        except error.HTTPError as exh:
            if exh.code == 404:
                self.trace('Curl: code 404: Page {0} non trouvée !'.format(url))
            else:           
                self.trace('Curl: La requête HTTP vers {0} a échoué avec le code {1} ({2})'.format(url,exh.code, exh.msg))
            raise exh
        except error.URLError as exu:
            self.trace('Curl: Echec d\'accès à %s Cause: %r'.format(url,exu.reason))
            raise exu
        return resp
    
    def secureRequest(self, url, method='GET', reqparams=None ,headers={}, paramsRetry=None):
        if paramsRetry is not None:
            timeout=int(paramsRetry['timeout'])
            nbRetries=int(paramsRetry['nbRetries'])
            arret=False
            essaiNo=1
            restResponse=None
            exceptionFinale=None
            while not arret:
                try: 
                    self.trace('Curl: lancement de la tentative: {0}/{1}'.format(essaiNo,nbRetries))
                    restResponse=self.getUrlResponseData(url, method, reqparams, headers)
                    self.trace('Curl: La tentative: {0}/{1} d\'est déroulée avec succès'.format(essaiNo,nbRetries))
                    arret=True
                except (error.URLError, error.HTTPError) as e:
                    self.trace('exception levee, on relance la requete')
                    essaiNo+=1
                    arret=not(essaiNo<=nbRetries)
                    if arret:
                        exceptionFinale=e
                    else:
                        self.trace('Curl: On attend {0} secondes avant la prochaine tentative no {1}/{2}'.format(timeout,essaiNo,nbRetries))
                        sleep(timeout) #on suspend l'exécution un ceraint nombre de secondes avant de réessayrr
            if exceptionFinale is not None:
                raise exceptionFinale
            else:
                return restResponse
        else:
            return self.getUrlResponseData(url, method, reqparams)

if __name__ == '__main__':
    c=Curl()
    #first we get a token using a simple GET MEthod !!!
    token=c.secureRequest('http://dru8rif.ovh/rest/session/token', paramsRetry={'timeout':3,'nbRetries':5})
    print('le csrf token vaut: {0}'.format(token))
    #we then use that token as well as authetication credentials to create a custom node in Drupal 8 through its REST POST interface
    a=Authentication('adminD8Rif','php39Rando57')
    hal_json_d8_postdata={"_links":{"type":{"href":"http://dru8rif.ovh/rest/type/node/randonnee_de_journee"}},
                       "title":[{"value":"Un autre p'tit tour à Bleau"}],
                       "uid":[{"target_id":"1","url":"\/fr\/user\/1"}],
                       "body":[{"value":"Un plus grand Parcours vallonné par le village de Recloses et les Demoiselles. Dénivelés.","format":"basic_html","summary":""}],
                       "field_date":[{"value":"2016-03-31"}],
                       "field_gare_depart":[{"value":"Paris Gare de Lyon"}],
                       "field_gare_depart_retour":[{"value":"Bourron Marlotte Grez (zone 5)"}],
                       "field_heure_arrivee_aller":[{"value":"2016-03-31T09:17:00"}],
                       "field_heure_depar":[{"value":"2016-03-31T08:19:00"}]}
    d8_post_headers={'Accept':'application/hal+json',
                     'Content-Type':'application/hal+json',
                     'X-CSRF-Token':token,
                     'Authorization':a.createBasicAuthorizationHeader()}
    d8_insertion=c.secureRequest('http://dru8rif.ovh/entity/node?_format=hal_json', method='POST',
                                 reqparams=hal_json_d8_postdata,headers=d8_post_headers,
                                 paramsRetry={'timeout':3,'nbRetries':5})
    