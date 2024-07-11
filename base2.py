import csv
import glob
import re
import ast
from datetime import datetime
from time import strftime
condition=1 #conditia pentru incheierea programului
dict = {} #initializarea dictionarului
memoryloadtxt = []
memoryloadcsv = []
wrote=1

def countmemory(memorie):
    ree(memorie)
    return sum(1 for element in memorie if element)

def ree(memorie):
    for element in reversed(memorie):
        if not element:
            memorie.remove(element)

def get_latest_file(extension):
    pattern = f"ListaCursanti.{extension} *.{extension}"
    files = glob.glob(pattern)

    regex = re.compile(rf'ListaCursanti\.{extension} (\d{{4}})_(\w+)_(\d{{2}})_(\d{{2}})_(\d{{2}})\.{extension}')
    file_dates = []

    for file in files:
        match = regex.search(file)
        if match:
            year, month, day, hour, minute = match.groups()
            month = datetime.strptime(month, "%B").month
            file_datetime = datetime(int(year), month, int(day), int(hour), int(minute))
            file_dates.append((file_datetime, file))

    file_dates.sort(key=lambda x: x[0], reverse=True)
    return file_dates[0][1] if file_dates else None


def read_dictionaries_from_file(filename, extension):
    if filename is not None:
        if(extension == 'txt'):
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        memoryloadtxt.append(ast.literal_eval(line))
        if(extension == 'csv'):
            fieldnames = ['id', 'name', 'prenume', 'cnp']
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=fieldnames)
                for row in reader:
                    if(row['id']):
                        d = dict.fromkeys(['id', 'cnp', 'name', 'prenume'], [])
                        d['id'] = row['id']
                        d['cnp'] = row['cnp']
                        d['name'] = row['name']
                        d['prenume'] = row['prenume']
                        memoryloadcsv.append(d)
    else:
        return 0


def lastid(memorie):
    x = {}
    if len(memorie)>0:
        for i in memorie:
            x = memorie[-1].copy()
        return x['id']
    else: return 0

def loadinmemory():
    global latest_txt_file
    latest_txt_file = get_latest_file("txt")
#    print(f"The latest .txt file is: {latest_txt_file}")
    read_dictionaries_from_file(latest_txt_file, 'txt')

    global latest_csv_file
    latest_csv_file = get_latest_file("csv")
#    print(f"The latest .csv file is: {latest_csv_file}")
    read_dictionaries_from_file(latest_csv_file, 'csv')


session = strftime(" %Y_%B_%d_%H_%M.txt")
sessioncsv = strftime(" %Y_%B_%d_%H_%M.csv")
def salvareintxt(memorie):
    global wrote
    f = open("ListaCursanti.txt" + session, mode="w",
             encoding="utf-8")  # generam un fisier f, in modul append unde scriem datele din dictionar
    f.write("\n")
    for i in range(countmemory(memorie)):
        f.write(str(memorie[i]))
        f.write("\n")
    if wrote == 0:
        f.write(str(dict))
    f.close()
    memorie.clear()
    loadinmemory()
    wrote = 1


def salvareincsv(memorie):
    if(wrote == 1):
        with open('ListaCursanti.csv' + sessioncsv, 'w') as g:  # functie de scriere in document de tip CSV
            fieldnames = ['id', 'nume', 'prenume', 'cnp']
            writer = csv.DictWriter(g, dialect='excel', fieldnames=fieldnames)
            for i in range(countmemory(memorie)):
                x = memorie[i].copy()
                writer.writerow({'id': x['id'], 'nume': x['name'], "prenume": x['prenume'], "cnp": x['cnp']})
    else: print("Ultimul participant nu a fost salvat")


def deleteid(memorie, stergere):
    for i in range(countmemory(memorie)-1):
        d = memorie[i].copy()
        print("id:",d['id'], "a fost pregatit de verificare de stergere \n")
        idd= int(d['id'])
        print(idd)
        print(stergere)
        if idd == int(stergere):
            print("id ",idd," a fost sters")
            memorie.remove(memorie[i])


def deletecnp(memorie, stergere):
    for i in range(countmemory(memorie)-1):
        d = memorie[i].copy()
        print("cnp:",d['cnp'], "a fost pregatit de verificare de stergere \n")
        idd= int(d['cnp'])
        print(idd)
        print(stergere)
        if idd == int(stergere):
            print("cnp ",idd," a fost sters")
            memorie.remove(memorie[i])
            return 0


def deleteduplicate(memorie):
    for i in range(0,countmemory(memorie)-1,1):
        for j in range(countmemory(memorie)-2,0,-1):
            x = memorie[i].copy()
            y = memorie[j].copy()
            print("id:",x['id']," si ",y['id']," au fost pregatite de verificare")
            if x['name'] == y['name'] and x['prenume']== y['prenume'] and x['cnp'] == y['cnp'] and i != j:
                print("id:", y['id'], " este un dublicat care a fost sters \n")
                memorie.remove(memorie[j])
                return 0
def reid(memorie):
    for i in range(0,countmemory(memorie)-1,1):
        for j in range(countmemory(memorie)-2,0,-1):
            x = memorie[i].copy()
            y = memorie[j].copy()
            print("id:",x['id']," si ",y['id']," au fost pregatite de verificare")
            if x['id'] == y['id'] and i != j:
                print("id:", y['id'], " este un id dublat \n")
                y['id'] = int(x['id']) + 1
                memorie[j]['id'] = y['id']


# ------ Functii Validare Date introduse
def scriereindictionar(data):
    inputdata=data
    input_data = inputdata.split()
    lenght = data.count(" ") + 1
    if lenght >2 :
        prenume = []  # initializam prenumele
        middle = range(1, lenght - 1)  # luam range de la al 2lea element pana la penultimul
        loadinmemory()
        dict['id'] = int(lastid(memoryloadtxt))+1
        memoryloadtxt.clear()
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
    control = 0
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
                print(cnp)
                print(" ",control)
                return 0
        else:
            print("01.Datele introduse sunt gresite: CNP nu are lungimea corespunzatoare")
            return 0
    else:
        print("00.Datele introduse sunt gresite: CNP nu este un numar")
        return 0


# ------ Functie apelare meniu
def main():
    print("Fisiere------------------------------")
    latest_txt_file = get_latest_file("txt")
    print(f"The latest .txt file is: {latest_txt_file}")
    latest_csv_file = get_latest_file("csv")
    print(f"The latest .csv file is: {latest_csv_file}")

    print("\nMeniu--------------------------------")
    print("1.Introduce datele unei noi persoane")
    print("2.Salveaza")
    print("3.Afiseaza Memorie")
    print("4.Stergere/Reformatare date")
    print("5.Inchidere")


    menu = input("Meniu:") #citirea tastei apasata pentru fiecare optiune din meniu
    match menu:
        case "1":
            print("Alegeti Optiunea:")
            print("1. Introducere manuala")
            print("2. Import din fisier CSV")
            menu1 = input("Meniu afisare:")
            match menu1:
                case "1":
                    print("Introduceti Nume Prenume CNP")
                    date = input()
                    if (scriereindictionar(date) != 0):
                        if (validaredate() == 1):
                            if (validarecnp() == 1):
                                print("Datele introduse sunt corecte")
                                global wrote
                                wrote = 0
                                scriereindictionar(date)
                    elif (scriereindictionar(date) == 0):
                        print("06. Multiple erori detectate")
                        global condition
                        condition = 0
                case "2":
                    print("Importing from csv....")
                    print(memoryloadcsv)
                    loadinmemory()
                    for i in range(len(memoryloadcsv)-1):
                        d = dict.fromkeys(['id', 'cnp', 'name', 'prenume'], [])
                        d['id'] = memoryloadcsv[i]['id']
                        d['cnp'] = memoryloadcsv[i]['cnp']
                        d['name'] = memoryloadcsv[i]['name']
                        d['prenume'] = memoryloadcsv[i]['prenume']
                        memoryloadtxt.append(d)
                    salvareintxt(memoryloadtxt)
                    salvareincsv(memoryloadtxt)

        case "2":
            print("Alegeti Optiunea:")
            print("1. Salveaza in fisier txt")
            print("2. Salveaza in fisier csv")
            print("3. Salveaza in csv+txt")
            menu2 = input("Meniu afisare:")
            match menu2:
                case "1":
                    memoryloadtxt.clear()
                    loadinmemory()
                    salvareintxt(memoryloadtxt)
                    memoryloadtxt.clear()
                case "2":
                    memoryloadtxt.clear()
                    loadinmemory()
                    salvareincsv(memoryloadtxt)
                    memoryloadtxt.clear()
                case "3":
                    memoryloadtxt.clear()
                    loadinmemory()
                    salvareintxt(memoryloadtxt)
                    salvareincsv(memoryloadtxt)
                    memoryloadtxt.clear()
        case "3":
            print("Alegeti Optiunea:")
            print("1. Afiseaza participantul curent")
            print("2. Afiseaza participantii inregistrati")
            menu3= input("Meniu afisare:")
            match menu3:
                case "1":
                    print(dict) #afisam datele din dictionar
                case "2":
                    memoryloadtxt.clear()
                    memoryloadcsv.clear()
                    loadinmemory()
                    print("----memorie txt\n")
                    print(memoryloadtxt)
                    print("----memorie csv\n")
                    print(memoryloadcsv)
                    memoryloadcsv.clear()
                    memoryloadtxt.clear()
        case "4":
            print("Alegeti Optiunea:")
            print("1. Sterge cursant dupa ID")
            print("2. Sterge cursant dupa CNP")
            print("3. Verificare si stergere dublicate")
            menu4 = input("Meniu afisare:")
            match menu4:
                case "1":
                    id = input("Scrie ID ce urmeaza sa fie sters:")
                    memoryloadtxt.clear()
                    loadinmemory()
                    deleteid(memoryloadtxt, id)
                    salvareintxt(memoryloadtxt)
                    memoryloadtxt.clear()
                case "2":
                    cnp = input("Scrie CNP ce urmeaza sa fie sters:")
                    memoryloadtxt.clear()
                    loadinmemory()
                    deletecnp(memoryloadtxt, cnp)
                    salvareintxt(memoryloadtxt)
                    memoryloadtxt.clear()
                case "3":
                    memoryloadtxt.clear()
                    loadinmemory()
                    for i in range(countmemory(memoryloadtxt)):
                        deleteduplicate(memoryloadtxt)
                    salvareintxt(memoryloadtxt)
                    salvareincsv(memoryloadtxt)
                    memoryloadtxt.clear()
                case "4":
                    memoryloadtxt.clear()
                    loadinmemory()
                    reid(memoryloadtxt)
                    salvareintxt(memoryloadtxt)
                    memoryloadtxt.clear()
        case "5":
            condition = 0  # inchidem programul

# ------ Pornire Loop program
while condition>0:
    main()