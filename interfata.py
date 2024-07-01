import tkinter as tk
import csv
dict = {} #initializare dictionar
def check(nume,prenume, cnp): # functia de verificare a datelor introduse
    error00.pack_forget() #stergerea mesajelor de eroare folosite in executia anterioara
    error01.pack_forget()
    error02.pack_forget()
    error03.pack_forget()
    error04.pack_forget()
    error05.pack_forget()

    check = 0
    ccnp=str(cnp)
    if cnp.isdigit() == 0: #verificam daca cnp ul este facut strict din cifre
        error00.pack()
    else: check=check+1 # incrementam check in cazul in care data este validata
    specialcharac = "+@!?!/123456789" #caracterele interzise
    if any(c in specialcharac for c in nume): #verificam daca se regasesc in nume
        error02.pack()
    else:
        check = check + 1# incrementam check in cazul in care data este validata
    if any(c in specialcharac for c in prenume): #verificam daca se regasesc in prenume
        error03.pack()
    else:
        check = check + 1# incrementam check in cazul in care data este validata

    if len(ccnp) == 13: #verificam nr de caractere a cnp ului
        controlnr = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9] #scriem nr de control a cnpu
        sumcontrol = 0
        for i in range(12):
            sumcontrol += controlnr[i] * int(ccnp[i]) #inmultim fiecare cifra din cnp cu cifra de control si o adunam in contor
        control = sumcontrol % 11 #scoatem restul impartirii la 11
        if control == 10: #in cazul in care restul e 10, cifra de control este 1
            control = 1
        if int(ccnp[12]) == control: #verificam cifra de control cu cifra calculata conform formulei
            check = check + 1 # incrementam check in cazul in care data este validata
        else:
            error04.pack()
    else:
        error01.pack()
    if(len(nume)==0):
        error05.pack()
    elif(len(prenume)==0):
        error05.pack()
    elif(len(cnp)==0):
        error05.pack()
    else:
        check=check+1
    if check == 5:
        verified.pack()
        dict['verified'] = 1 #adaugam check ul de date verificate in dictionar

def writetext(): #functie scriere in fisier txt
    wrotetotext.pack_forget() #stergem mesajele de scriere anterioara a altor date
    wrotetocsv.pack_forget()
    dict['nume'] = textbox.get()
    dict['prenume'] = textbox2.get()
    dict['cnp'] = textbox3.get()
    cnp = dict['cnp']
    prenume = dict['prenume']
    nume = dict['nume']  #efectuam citirea din textboxuri
    dict['verified'] = 0
    check(nume, prenume, cnp) #trecem prin functia de verificare
    if(dict['verified'] == 1): #daca este verificata functia, o vom scrie in folderul txt
        with open("test_scriere.txt", 'a') as f:
            f.write("\n")
            f.write(str(dict))
            f.close()
            textbox.delete(0, 99) #golim textboxurile
            textbox2.delete(0, 99)
            textbox3.delete(0, 99)
            wrotetotext.pack() #afisam mesaj scriere

def writecsv(): #functie scriere in fisier csv
    wrotetotext.pack_forget() #stergem mesajele de scriere anterioara a altor date
    wrotetocsv.pack_forget()
    dict['nume'] = textbox.get()
    dict['prenume'] = textbox2.get()
    dict['cnp'] = textbox3.get()
    dict['verified']=0
    cnp = dict['cnp']
    prenume = dict['prenume']
    nume = dict['nume'] #efectuam citirea din textboxuri
    check(nume, prenume, cnp) #trecem prin functia de verificare
    if(dict['verified'] == 1): #daca este verificata functia, o vom scrie in folderul txt
        with open('names.csv', 'a') as g:
            fieldnames = ['nume', 'prenume', 'cnp']
            writer = csv.DictWriter(g, dialect='excel', fieldnames=fieldnames)
            writer.writerow({'nume': dict['nume'], "prenume": dict['prenume'], "cnp": dict['cnp']})
            wrotetocsv.pack() #afisam mesaj scriere
            textbox.delete(0, 99) #golim textboxurile
            textbox2.delete(0, 99)
            textbox3.delete(0, 99)

def quit():
    window.destroy() #inchidem fereastra

window = tk.Tk()
window.title("Cursant nou") #titlu fereastra
window.geometry("500x300") #rezolutie fereastra
numet = tk.Label(text = "Nume") # label textbox1
prenumet = tk.Label(text = "Prenume") #label textbox2
CNPt = tk.Label (text = "CNP") # label textbox 3
error00 = tk.Label(text = "00.Datele introduse sunt gresite: CNP nu este un numar",fg="red")  #label erori
error01 = tk.Label(text = "01.Datele introduse sunt gresite: CNP nu are lungimea corespunzatoare",fg="red")
error02 = tk.Label(text = "02.Datele introduse sunt gresite: Numele contine caractere interzise/cifre",fg="red")
error03 = tk.Label(text = "03.Datele introduse sunt gresite: Prenumele contine caractere interzise/cifre",fg="red")
error04 = tk.Label(text = "04.Datele introduse sunt gresite: CNP nu este in format corect",fg="red")
error05 = tk.Label(text = "05. Nu au fost introduse elementele necesare", fg="red")
wrotetotext = tk.Label(text ="Datele au fost salvate in format txt",fg="green") #label confirmari
wrotetocsv = tk.Label(text="Datele au fost salvate in format csv",fg="green")
verified = tk.Label(text = "Datele sunt corecte")
textbox = tk.Entry(window, width = 20) #cutie textbox
textbox2 = tk.Entry(window, width = 20)
textbox3 = tk.Entry(window, width = 20)

butontxt = tk.Button (window, text = "Salveaza datele", command = writetext  ) #butoanele si functiile pe care le apeleaza
butoncsv = tk.Button (window, text = "Salveaza csv", command = writecsv )
exit = tk.Button (window, text = "Exit", command = quit)

numet.pack() #activarea prin "pack"
textbox.pack()
prenumet.pack()
textbox2.pack()
CNPt.pack()
textbox3.pack()
butontxt.pack()
butoncsv.pack()
exit.pack()

window.mainloop() #mentinerea fisierului in loop