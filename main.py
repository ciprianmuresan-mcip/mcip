# 1.
nrsol=0 #numarul de solutii

def afis(x): # afiseaza valorile din lista x (solitia)
    global nrsol # ca sa vada pe nrsol
    sol="" # construiesc solutia pe un singur rand
    for i in range(len(x)):
        sol=sol+str(x[i])+" "
    print (sol)
    nrsol=nrsol+1

def back(coins, x, S, sp):
    for i in range(len(coins)): #ia fiecare noneda
        if len(x)==0 or coins[i]>x[len(x)-1]: # daca e prima sau are valoare mai mare decat ultima pusa (ca sa nu repete monede si sa nu permute solutia)
            x.append(coins[i]) #adauga moneda la solutie
            sp=sp+coins[i] #aduna moneda la suma partiala platita
            if sp<=S: # nu s-a depasit suma de palta
                if sp==S: # este exact suma de plata
                    afis(x) # afisare
                else:
                    back(coins,x,S,sp) # continua
            x.pop(len(x)-1) # scoate ultima moneda pusa pt ca se depaseste suma
            sp=sp-coins[i] # scade din suma moneda pusa pt ca sedepaseste suma

def back_i(coins, x, S):
    sp=0
    k=0
    while k>=0:
        ok=0
        for i in range(len(coins)-1): #ia fiecare noneda
            if len(x)==0 or coins[i]>x[len(x)-1]: # daca e prima sau are valoare mai mare decat ultima pusa (ca sa nu repete monede si sa nu permute solutia)
                x.append(coins[i]) #adauga moneda la solutie
                sp=sp+coins[i] #aduna moneda la suma partiala platita
                print (x[k])
                if sp<=S: # nu s-a depasit suma de palta
                    if sp==S: # este exact suma de plata
                        afis(x) # afisare
                    else :
                        ok=1
                        k=k+1
                else:
                    x.pop(len(x)-1) # scoate ultima moneda pusa pt ca se depaseste suma
                    sp=sp-coins[i] # scade din suma moneda pusa pt ca sedepaseste suma
        if ok==0:
           # x.pop(len(x)-1) # scoate ultima moneda pusa pt ca se depaseste suma
            #sp=sp-coins[i] # scade din suma moneda pusa pt ca sedepaseste suma
            k=k-1


coins=[2,3,5,7,11,13] #valorile monedelor
S=15  # suma de plata
#S=1600 - pt imposibil
x=[]  # solutia (lista monedelor folosite)
back(coins,x,S,0)
#back_i(coins, x,S)
if nrsol==0:
    print ("Impossible")