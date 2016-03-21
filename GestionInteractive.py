# -*- coding: utf-8 -*-
#!/usr/bin/python

import argparse
from presentation.AnimateursFrame import AnimateursF
from Tkinter import Tk

def parseOptions():
    #cf. http://docs.python.org/library/argparse.html#module-argparse
    #cf. http://docs.python.org/dev/library/argparse.html
    p = argparse.ArgumentParser(description='extract from adherent website and insert update or delete randonnee or put Stats in ACCESS.')
    p.add_argument('--env', '-e', default='prod', help='decides the dev or production environment')
    options = p.parse_args()
    return options

if __name__ == "__main__":
    options=parseOptions()
    env=u'%s' %(options.env)
    root = Tk()
    #root.geometry("800x800+300+300")
    app = AnimateursF(root,env=env)
    root.mainloop()
    