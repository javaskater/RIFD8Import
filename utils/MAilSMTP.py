# -*- coding: utf-8 -*-

#!/usr/bin/env python
import codecs
from email import Encoders
import os
import smtplib

from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate


# Import smtplib for the actual sending function
# Import the email modules we'll need
class RIFMail:
    def __init__(self,smtpServer):
        self.s=smtplib.SMTP(smtpServer)
        self.msg=""
        #gestion de type liste
        self.fics_joints=[]
    
    def ajouteFichierDansContenu(self,path_fic):
        titremsg = "Contenu du fichier: "+os.path.basename(path_fic)+"\n"
        fp = codecs.open(path_fic, "r", 'utf-8')
        localmsg=fp.read()
        self.msg = u"%s%s%s" %(self.msg,titremsg,localmsg)
        fp.close;
    
    def jointFichier(self,path_fic,type='rb'):
        donnees={'path':path_fic,'type':type}
        self.fics_joints.append(donnees)
            
    def envoie(self,moi,eux,titre,msgbody=None):
        mimemsg = MIMEMultipart()
        mimemsg['From'] = moi
        mimemsg['Return-Path'] = moi
        mimemsg['To'] = COMMASPACE.join(eux)
        mimemsg['Date'] = formatdate(localtime=True)
        mimemsg['Subject'] = titre
        if msgbody is not None:
            self.msg = "%s\n\n%s" %(unicode(msgbody,'utf-8'),self.msg)
        mimemsg.attach(MIMEText(self.msg,'plain','utf-8'))
        for donnees_fichier in self.fics_joints:
             part = MIMEBase('application', "octet-stream")
             part.set_payload( open(donnees_fichier['path'],donnees_fichier['type']).read() )
             Encoders.encode_base64(part)
             part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(donnees_fichier['path']))
             mimemsg.attach(part)
        self.s.sendmail(moi, eux,mimemsg.as_string())
        self.s.close()


if __name__ == "__main__":
    moi="pythonrubylang@gmail.com"
    eux=["jeanpierre.mena@gmail.com","jeanpierre.mena@free.fr"]
  
    rifmail=RIFMail("smtp.free.fr")
    rifmail.ajouteFichierDansContenu("Log.py")
    rifmail.jointFichier("../test.py","r")
    rifmail.jointFichier("../test.sxw")
    rifmail.envoie(moi, eux, "test envoi de 2 fichiers")
