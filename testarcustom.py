from tkinter import *
import psycopg2
import os

class interface:
    def __init__(self,app):

        pastaapp = os.path.dirname(__file__)

        imageteste = PhotoImage(file=pastaapp+"\\download.gif")

        self.btnaperte = Button(app,image=imageteste)
    
    


janela = Tk()
app = interface(janela)

janela.geometry("400x500")
janela.iconbitmap("5309792.png")
janela.configure(background="#151515")
janela.configure()
janela.mainloop()