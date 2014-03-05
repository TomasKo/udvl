# Toto je ukazkovy program, ktory ukazuje ako vytvorit vstup pre SAT solver,
# spustit ho a precitat a rozparsovat jeho vystup. Mozete ho skludom pouzit
# ako kostru vasho riesenia.
#
# Tento program predpoklada, ze minisat / minisat.exe
# sa nachadza
# - Linux: v adresari, kam ukazuje PATH
# - Windows: v adresari, kam ukazuje PATH, alebo v akt. adresari
# Podla potreby upravte cestu v premennej CESTA_K_MINISAT

import os

CESTA_K_MINISAT = "minisat"
n=0

def q(i,j):
    return i*n+j+1

# Pomocna funkcia na zapis implikacie do suboru
def impl(subor, a, b):
    subor.write( "{0:d} {1:d} 0\n".format(-a, b) )

   
# Funkcia zapisujuca problem do vstupneho suboru SAT solvera v spravnom formate
def zapis_problem(subor):
    # v kazdom riadku je aspon jrdna dama
    for i in range(n):
        for j in range(n):
            subor.write("{0:d} ".format(q(i,j)))
        subor.write("0\n")
        
    # v kazdom riadku je najviac jrdna dama
    for i in range(n):
        for j1 in range(n):
            for j2 in range(n):
                if j1!= j2:
                    impl(subor,q(i,j1),-q(i,j2))
                    
    # v kazdom stlpci je najviac jrdna dama
    for j in range(n):
        for i1 in range(n):
            for i2 in range(n):
                if i1!= i2:
                    impl(subor,q(i1,j),-q(i2,j))
                    for k in range(n):
                        if ((j+i1)==(k+i2))or((j-i1)==(k-i2)):
                            impl(subor,q(j,i1),-q(k,i2))
                            
    
    # na kazdej uhlopriecke je najviac jedna dama
    
    

# Funkcia vypisujuca riesenie najdene SAT solverom z jeho vystupneho suboru
def vypis_riesenie(ries):
    # rozbijeme riesenie na cisla/premenne
    vs = ries.split()
    # zahodime ukoncovaciu 0
    vs = vs[0:-1]
    # vypiseme vyznam riesenia
    i=1
    for v in vs:
        v = int(v)
        if v>0:
            print("{:1}{:2}".format((v-1)%n,(v-1)//n))
            #print("{:1}{:1}{:3}{:5}".format(i,". dama",(v-1)%n,(v-1)//n))
            i+=1

def main():
    # Normalne by sme tu mozno nieco nacitavali zo standardneho vstupu,
    # ale tato uloha nema ziadny vstup.
    global n
    n=int(input());

    # otvorime subor, do ktoreho zapiseme vstup pre sat solver
    try:
        with open("vstup.txt", "w") as o:
            # zapiseme nas problem
            zapis_problem(o)
    except IOError as e:
        print("Chyba pri vytvarani vstupneho suboru ({0}): {1}".format(
                e.errno, e.strerror))
        return 1

    # spustime SAT solver
    os.system("{} vstup.txt vystup.txt".format(CESTA_K_MINISAT));

    # nacitame jeho vystup
    try:
        with open("vystup.txt", "r") as i:
            # prvy riadok je SAT alebo UNSAT
            sat = i.readline()
            if sat == "SAT\n":
                print("Riesenie:")
                # druhy riadok je riesenie
                ries = i.readline()
                vypis_riesenie(ries)
            else:
                print("Ziadne riesenie")
    except IOError as e:
        print("Chyba pri nacitavani vystupneho suboru ({0}): {1}".format(
                e.errno, e.strerror))
        return 1

    return 0

if __name__ == "__main__":
    main()
