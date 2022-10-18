from lib2to3.pgen2.tokenize import generate_tokens
import tkinter
from tkinter import *
from dynamic_AVTRNG import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import hashlib
import numpy as np
from pyautogui import typewrite



#wygeneruj klucz
# def generateValue():
#     s=1
    
#     number=trng()
    
# number=trng()    
# key = RSA.generate(2048, None, number)

# privateKeyPEM = key.export_key()
# public_keyPEM = key.publickey().export_key()
# public_key = key.publickey()



class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Pierwsza wiadomość')
        self.lbl2=Label(win, text='Druga wiadomosc')
        self.text1=Label(win, text='Wiadomosc po zahashowaniu')
        self.text2=Label(win, text='Wiadomosc po zakodowaniu')
        self.text3=Label(win, text='Wiadomosc po odkodowaniu')
        self.text4=Label(win, text='Wiadomosc po zahashowaniu')
        
        self.text7=Label(win, text='Poprawnosc oryginalnej wiadomosci z oryginalym kluczem')
        self.text8=Label(win, text='Poprawnosc zmienionej wiadomosci z oryginalnym kluczem')
        self.text9=Label(win, text='Poprawnosc oryginalnej wiadomosci z innym kluczem')

        self.text10=Label(win, text='-')
        self.text11=Label(win, text='-')
        self.text12=Label(win, text='-')
        self.text13=Label(win, text='-')
        
        self.text16=Label(win, text='-')
        self.text17=Label(win, text='-')
        self.text18=Label(win, text='-')
        self.text19=Label(win, text='-')

        self.t1=Entry()
        self.t2=Entry()
        

        self.text1.place(x=50, y=120)
        self.text2.place(x=50, y=150)
        self.text3.place(x=50, y=180)
        self.text4.place(x=50, y=290)
        
        self.text7.place(x=50, y=390)
        self.text8.place(x=50, y=410)
        self.text9.place(x=50, y=430)

        self.text10.place(x=230, y=120)
        self.text11.place(x=230, y=150)
        self.text12.place(x=230, y=180)
        self.text13.place(x=230, y=290)
        
        self.text16.place(x=400, y=390)
        self.text17.place(x=400, y=410)
        self.text18.place(x=400, y=430)
        self.text19.place(x=200, y=25)

        self.lbl1.place(x=50, y=60)
        self.t1.place(x=50, y=90)

        self.lbl2.place(x=50, y=230)
        self.t2.place(x=50, y=260)

        self.b1=Button(win, text='Generuj klucz')
        self.b2=Button(win, text='Hashuj')
        self.b3=Button(win, text='Hashuj')
        self.b1.bind('<Button-1>', self.generateKey)
        self.b2.bind('<Button-1>', self.hashuj1)
        self.b3.bind('<Button-1>', self.hashuj2)
        self.b1.place(x=50, y=25)
        self.b2.place(x=300, y=90)
        self.b3.place(x=300, y=260)
        

    def hashuj1(self,string):
        global HEX_DIGG
        global decryptedG
        global key

        trueMessage=self.t1.get()
        #hashowanie
        hash_object = hashlib.sha256(str.encode(self.t1.get()))
        #zmiana na hex
        hex_dig = hash_object.hexdigest()
        #wypisanie
        self.text10['text']=str(hex_dig)
        #koder
        encryptor = PKCS1_OAEP.new(public_key)
        #kodowanie
        encrypted = encryptor.encrypt(str.encode(hex_dig))
        #wypisanie
        self.text11['text']=str(binascii.hexlify(encrypted))
        #dekoder
        decryptor = PKCS1_OAEP.new(key)
        #dekodowanie
        decrypted = decryptor.decrypt(encrypted)
        #wypisanie
        self.text12['text']=str(decrypted.decode("utf-8"))

        
        HEX_DIGG = hex_dig
        decryptedG = decrypted


    def hashuj2(self,string):

        fakeMessage = self.t2.get()
        hash_object2 = hashlib.sha256(str.encode(fakeMessage))
        hex_dig2 = hash_object2.hexdigest()
        self.text13['text']=str(hex_dig2)

        #wypisanie obok Sprawdzenie oryginalnej wiadomości z oryginalnym kluczem
        if (HEX_DIGG == decryptedG.decode("utf-8")):
            
            self.text16['text']="Hashe są takie same"
        else:
            self.text16['text']="Hashe są różne"

        #wypisanie obok Sprawdzenie zmienionej wiadomości z oryginalnym kluczem
        if (hex_dig2 == decryptedG.decode("utf-8")):
            self.text17['text']="Hashe są takie same"
        else:
            self.text17['text']="Hashe są różne"

        #randomowy klucz
        key2 = RSA.generate(2048)
        decryptor2 = PKCS1_OAEP.new(key2)
        
        ##wypisanie obok Sprawdzenie oryginalnej wiadomości z innym kluczem
        try:
            decrypted2 = decryptor2.decrypt(encrypted)
            self.text18['text']="Decrypted->"+decrypted2
        except:
            self.text18['text']="Nie udana próba rozkodowania wiadomości inym kluczem"


    def generateKey(self,event):
        global HEX_DIGG
        global decryptedG
        global encrypted
        global public_key
        global key

        number=trng()
        self.text19['text']="Czeka na wygenerowanie klucza"
        for x in number:
            key = RSA.generate(2048,x)
        

        #tworzenie kluczy
        public_key = key.publickey()
        HEX_DIGG, decryptedG, encrypted = "", "", ""
        
        self.text19['text']="Wygenerowany"
    


window=Tk()
mywin=MyWindow(window)
window.title('Cyfrowy podpis ')
window.geometry("720x480+10+10")
window.mainloop()