import csv

condition=1 #conditia pentru incheierea programului
dict = {} #initializarea dictionarului
while condition>0: #pornirea programului in mod repetat
    print("1.Introduce datele unei noi persoane")
    print("2.Salveaza")
    print("3.Afiseaza Dictionar")
    print("4.Inchide")
    print("5.Salveaza ca fisier csv")
    print("SALVEAZA (salveaza si inchide programul)")
    menu = input("Meniu:") #citirea tastei apasata pentru fiecare optiune din meniu
    match menu:
        case "1":
            print("Introduceti Nume Prenume CNP")
            initialinput = input() #citirea inputului datelor cerute
            input_data = initialinput.split() #separarea inputului in stringuri individuale
            lenght = initialinput.count(" ") + 1 #verificarea numarului de cuvinte
            if lenght<2: #verificam daca am introdus numarul minim de 3 elemente - nume prenume cnp
                print("05. Nu au fost introduse elementele necesare")
            else:
                lenghtprenume = lenght - 2 #obtinem numarul de prenume prin scaderea nr 1 pentru elementul nume si 1 pt cnp
                prenume = []   #initializam prenumele
                middle = range(1, lenght - 1, 1) #luam range de la al 2lea element pana la penultimul
                check = 0
                for i in middle:
                    prenume.append(input_data[i]) #adaugam fiecare prenume in o lista

                nume = input_data[0] # preluam numele intr-o variabila nume
                cnp = input_data[lenght - 1] #preluam cnp in variabila cnp

                # ---------validare
                if cnp.isdigit() == 0: # verificam daca tot cnp ul este format din cifre, daca nu afisam eroare
                    print("00.Datele introduse sunt gresite: CNP nu este un numar")
                else: # crestem contorul check in caz ca este in format corect
                    check = check + 1

                # -
                if len(cnp) != 13: #verificam daca cnp are lungimea de 13 caractere, daca nu afisam eroare
                    print("01.Datele introduse sunt gresite: CNP nu are lungimea corespunzatoare")
                else: # crestem contorul check in caz ca este in format corect
                    check = check + 1
                # -
                specialcharac = "+@!?!/123456789" #lista de caractere ilegale
                if any(c in specialcharac for c in nume): #verificam daca se regasesc in lista noastra de caractere)
                    print("02.Datele introduse sunt gresite: Numele contine caractere interzise/cifre")
                else:
                    check = check + 1 # crestem contorul check in caz ca este in format corect
                if any(c in specialcharac for c in prenume): # procedam la fel pentru prenume
                    print("03.Datele introduse sunt gresite: Prenumele contine caractere interzise/cifre")
                else:
                    check = check + 1 # crestem contorul check in caz ca este in format corect
                # -
                controlnr = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9] # 279146358279 este numarul dupa care se verifica cifra de control la CNP
                sumcontrol = 0
                for i in range(0, 12, 1):
                    sumcontrol = sumcontrol + controlnr[i] * int(cnp[i]) # efectuam inmultirea cifrelor din cnp si din nr de control si dupa le adunam
                control = sumcontrol % 11 #obtinem restul impartirii la 11
                if control == 10: #in cazul in care restul este 10, formula arata ca cifra de control va fi 1
                    control = 1
                if int(cnp[12]) == control: # in cazul in care e sub 10, cifra de control va fi respectiva cifra
                    print("Date Validate") #afisam ca datele de cnp sunt corecte
                    check = check + 1 # crestem contorul check in caz ca este in format corect
                else:
                    print("04.Datele introduse sunt gresite: CNP nu este in format corect")
                if check == 5: # daca s-au verificat toti cei 5 pasi trecem la scrierea in dictionar a datelor
                    dict['name'] = nume
                    dict['prenume'] = prenume
                    dict['cnp'] = cnp

        case "2":
            f = open("test_scriere.txt", mode="a", encoding="utf-8") #generam un fisier f, in modul append unde scriem datele din dictionar
            f.write("\n")
            f.write(str(dict))
            f.close()
        case "3":
            print(dict) #afisam datele din dictionar
        case "4":
            condition=0 # inchidem programul
        case "SALVEAZA":
            f = open("test_scriere.txt", mode="a", encoding="utf-8") # este o functie de save in text and exit
            f.write("\n")
            f.write(str(dict))
            f.close()
            condition = 0
        case "5":
            with open('names.csv', 'a') as g:  # functie de scriere in document de tip CSV
                fieldnames= ['nume','prenume','cnp']
                writer = csv.DictWriter(g, dialect='excel', fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'nume': dict['name'], "prenume": dict['prenume'], "cnp": dict['cnp']})
