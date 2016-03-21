# -*- coding: utf-8 -*-
#!/usr/bin/python

import argparse
from domain.Settings import SettingsImportRandosJour
from batch import RandoRestActions

def parseOptions():
    #cf. http://docs.python.org/library/argparse.html#module-argparse
    #cf. http://docs.python.org/dev/library/argparse.html
    p = argparse.ArgumentParser(description='extract from adherent website and insert update or delete randonnee or put Stats in ACCESS.')
    p.add_argument('--env', '-e', default='prod', help='decides the dev or production environment')
    p.add_argument('--act', '-a', default='xes', help='x for extracts (insert or update in ACCESS), d for delete, e for putting RjEfface to true ,s for getting statistics') #par défaut appelle l'extraction et la suppression
    options = p.parse_args()
    return options

if __name__ == "__main__":
    options=parseOptions()
    todo=u'%s' %(options.act)
    settings= SettingsImportRandosJour().options(u'%s' %(options.env))
    if todo is not None and len(todo) > 0:
        ra=RandoRestActions.RestActions(settings)
        for action in todo:
            if action == u'x': #on extrait les randonnées prises en charge
                logGene,xmlPath,xmlPathParseError,xmlPathPyODBCError = ra.extraitRadonneesJours()
                ra.mail_envoie_resultat()
            elif action == u'd': #on supprime physiquement de ACCESS les randonnées annulées (avec les animations associées)
                logGene,xmlPath,xmlPathParseError,xmlPathPyODBCError = ra.supprimeRadonneesJours()
                ra.emailTitre=u'Résultat de la suppression des randonnées de jour ...'
                ra.mail_envoie_resultat()
            elif action == u'e': #on met le bit Rj_Effacé ) true pour les randonnées annulées
                logGene,xmlPath,xmlPathParseError,xmlPathPyODBCError = ra.supprimeRadonneesJours(True)
                ra.emailTitre=u'Résultat de l\'effacement des randonnées de jour ...'
                ra.mail_envoie_resultat()
            elif action == u's': #insère les statistiques pour une randonnée
                logGene,xmlPath,xmlPathParseError,xmlPathPyODBCError = ra.extraitStatsRadonneeJours()
                ra.emailTitre=u'Résultat de la mise à jour des statistiques des randonnées de jour ...'
                ra.mail_envoie_resultat()