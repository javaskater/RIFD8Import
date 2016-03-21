# -*- coding: utf8 -*-
'''
Created on 28 avr. 2012

@author: jpmena
'''
from urllib import request, parse, error
from _datetime.datetime import time

class Curl(object):
    def __init__(self,f_log=None,proxy_info=None):
        self.proxy_support=None
        self.f_log=f_log
        #if(proxy_info is not None):
        #    self.proxy_support = urllib.ProxyHandler({"http":"http://%(host)s:%(port)d" % proxy_info})
    
    def trace(self,msg):
        if self.f_log is not None:
             self.f_log.p(msg)
        else:
            print(msg)
    
    #TODO ajouter l'authentification basique !!!
    def getUrlResponseData(self, url, method='GET', requestparams=None):
        resp=None
        try:
            #problème récupérer les données en utf-8
            #http://stackoverflow.com/questions/1020892/urllib2-read-to-unicode
            self.trace('Curl: requete de type {0}, pour l\'URL: {2}'.format(method,url))
            querystring=None
            if requestparams is not None:
                querystring = parse.urlencode(requestparams)
                for cle,valeur in requestparams :
                    self.trace('avec comme argument : {0} => {1}'.format(cle,valeur))
                    
            
            connection = {
                      'GET': lambda url: request.urlopen(url+'?' + querystring),
                      'POST': lambda url: request.urlopen(url, querystring.encode('ascii')),
                      }[method](url)
            
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
    
    def secureRequest(self, url, method, reqparams, paramsRetry=None):
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
                    restResponse=self.getUrlResponseData(url, method, reqparams)
                    self.trace('Curl: La tentative: {0}/{1} d\'est déroulée avec succès'.format(essaiNo,nbRetries))
                    arret=True
                except (error.URLError, error.HTTPError) as e:
                    self.trace('exception levee, on relance la requete')
                    essaiNo+=1
                    arret=not(essaiNo<=nbRetries)
                    if arret:
                        exceptionFinale=e
                    else:
                        self.trace('Curl: On attend {0} secondes avant la prochaine tentative no {1}/{1}'.format(timeout,essaiNo,nbRetries))
                        time.sleep(timeout) #on suspend l'exécution un ceraint nombre de secondes avant de réessayrr
            if exceptionFinale is not None:
                raise exceptionFinale
            else:
                return restResponse
        else:
            return self.getUrlResponseData(url, method, reqparams)

if __name__ == '__main__':
    c=Curl(proxy_info={'host':'dgproxy.appli.dgi','port':8080})
    c.connect({'urlLogin':u'http://testadh.rifrando.asso.fr/users/login/', 
                                         'user':[u'data[User][username]',u'196793'],
                                         'password':[u'data[User][password]',u'yvonne'],
                                         'nomCookie':u'CAKEPHP'})
    xml=c.getUrlResponseData(u'http://testadh.rifrando.asso.fr/randonnees/extractionstatistique54s5g7vd5d4f849ao5f4wsh')
    print xml