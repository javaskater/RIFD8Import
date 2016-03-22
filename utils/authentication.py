# -*- coding: utf8 -*-

'''
Created on 22 mars 2016

@author: jpmena
'''
import base64

class Authentication(object):

    def __init__(self, identifiant, mot_de_passe):
        self.identifiant = identifiant
        self.mot_de_passe = mot_de_passe
    
    def createBasicAuthorizationHeader(self):
        stringToEncode = '{0}:{1}'.format(self.identifiant, self.mot_de_passe)
        base64Encoded= base64.b64encode(str.encode(stringToEncode))
        return 'Basic {0}'.format(base64Encoded)


if __name__ == '__main__':
    a=Authentication('adminD8Rif','php39Rando57')
    print('header vaut: {0}'.format(a.createBasicAuthorizationHeader()))