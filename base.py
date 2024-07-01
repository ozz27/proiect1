import csv

condition=1 #conditia pentru incheierea programului
dict = {} #initializarea dictionarului


def salvareintxt():
    f = open("test_scriere.txt", mode="a",
             encoding="utf-8")  # generam un fisier f, in modul append unde scriem datele din dictionar
    f.write("\n")
    f.write(str(dict))
    f.close()


def salvareincsv():
    with open('names.csv', 'a') as g:  # functie de scriere in document de tip CSV
        fieldnames = ['nume', 'prenume', 'cnp']
        writer = csv.DictWriter(g, dialect='excel', fieldnames=fieldnames)
        writer.writerow({'nume': dict['name'], "prenume": dict['prenume'], "cnp": dict['cnp']})


def scriereindictionar(data):
    inputdata=data
    input_data = inputdata.split()
    lenght = data.count(" ") + 1
    if lenght >2 :
        prenume = []  # initializam prenumele
        middle = range(1, lenght - 1)  # luam range de la al 2lea element pana la penultimul
        dict['cnp'] = input_data[lenght - 1]
        for i in middle:
            prenume.append(input_data[i])  # adaugam fiecare prenume in o lista
        dict['name'] = input_data[0]
        dict['prenume'] = prenume
    else:
        print("05. Nu au fost introduse elementele necesare")
        return 0

def validaredate():
    specialcharac = "+@!?!/123456789"  # lista de caractere ilegale
    if any(c in specialcharac for c in dict['name']):  # verificam daca se regasesc in lista noastra de caractere)
        print("02.Datele introduse sunt gresite: Numele contine caractere interzise/cifre")
        return 0
    if any(c in specialcharac for c in dict['prenume']):  # procedam la fel pentru prenume
        print("03.Datele introduse sunt gresite: Prenumele contine caractere interzise/cifre")
        return 0
    return 1


def validarecnp():
    cnp=dict['cnp']
    if cnp.isdigit() == 1:
        if len(cnp) == 13:
            controlnr = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]  # 279146358279 este numarul dupa care se verifica cifra de control la CNP
            sumcontrol = 0
            for i in range(0, 12, 1):
                sumcontrol = sumcontrol + controlnr[i] * int(cnp[i])  # efectuam inmultirea cifrelor din cnp si din nr de control si dupa le adunam
                control = sumcontrol % 11  # obtinem restul impartirii la 11
                if control == 10:  # in cazul in care restul este 10, formula arata ca cifra de control va fi 1
                    control = 1
                if int(cnp[12]) == control:  # in cazul in care e sub 10, cifra de control va fi respectiva cifra
                    return 1  # afisam ca datele de cnp sunt corecte
                else:
                    print("04.Datele introduse sunt gresite: CNP nu este in format corect")
                    return 0
        else:
            print("01.Datele introduse sunt gresite: CNP nu are lungimea corespunzatoare")
            return 0
    else:
        print("00.Datele introduse sunt gresite: CNP nu este un numar")
        return 0

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
            date = input()
            scriereindictionar(date)
            if (scriereindictionar(date) != 0):
                if(validaredate()==1):
                    if(validarecnp()==1):
                        print("Datele introduse sunt corecte")
            elif(scriereindictionar(date) == 0):
                print("06. Multiple erori detectate")
                condition=0
        case "2":
            salvareintxt()
        case "3":
            print(dict) #afisam datele din dictionar
        case "4":
            condition=0 # inchidem programul
        case "SALVEAZA":
            salvareintxt()
            condition = 0
        case "5":
            salvareincsv()
