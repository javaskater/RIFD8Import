# -*- coding: utf8 -*-
#!/usr/bin/python
'''
Created on 27 déc. 2010

@author: jpmena
'''
import codecs
from datetime import datetime
import os, sys


class Log(object):
    log=None
    def __init__(self,log_path=None):
        self.log=None
        if log_path is not None:
            self.log_path=log_path
            if(os.path.exists(self.log_path)):
                os.remove(self.log_path)
                #self.log=open(self.log_path,'a')
                self.log=codecs.open(self.log_path, "a", 'utf-8')
    
    def getInstance(log_path=None):
        return Log.log
    
    getInstance=staticmethod(getInstance)
        
    
    def p(self,msg):
        aujour_dhui=datetime.now()
        date_stamp=aujour_dhui.strftime("%d/%m/%y-%H:%M:%S")
        #print sys.getdefaultencoding()
        unicode_str=u'%s : %s \n'  % (date_stamp,msg)
        #unicode_str=msg
        if self.log is not None:
            self.log.write(unicode_str)
        else:
            print(unicode_str)
        return unicode_str
    
    def raw(self,msg):
        aujour_dhui=datetime.now()
        date_stamp=aujour_dhui.strftime("%d/%m/%y-%H:%M:%S")
        #print sys.getdefaultencoding()
        unicode_str='%s : %s \n'  % (date_stamp,msg)
        #unicode_str=msg
        if self.log is not None:
            self.log.write(unicode_str)
        else:
            print(unicode_str)
        return unicode_str
    
    def close(self):
        if self.log is not None:
            self.log.flush()
            self.log.close()
        return self.log_path

if __name__ == '__main__':
    l=Log.getInstance()
    l.p("premier message de Log à accents")
    Log.getInstance().p("second message de Log")
    l.close()