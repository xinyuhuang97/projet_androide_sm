from gurobipy import *
from sm import gennere_set_f_m
female,male,s_f,s_m=gennere_set_f_m(5,6)
cote_optimal=male
pref_cote_opt=s_m
cote_dessimale=female
pref_cote_des=s_f


nb_opt=len(cote_optimal)
nb_des=len(cote_dessimale)
# Creation la liste de preference
#print(cote_dessimale)
list_pref_cote_opt=[]
list_pref_cote_des=[]
for i in range(nb_opt):
    l=[]
    #print(cote_optimal)
    lp=pref_cote_opt[cote_optimal[i]][1]
    for j in range(nb_des):
        #print(i)
        personne=cote_dessimale[j]
        index=lp.index(personne)
        score=nb_des-index
        l.append(score)
    list_pref_cote_opt.append(l)

for i in range(nb_des):
    l=[]
    lp=pref_cote_des[cote_dessimale[i]][1]
    for j in range(nb_opt):
        personne=cote_optimal[j]
        index=lp.index(personne)
        score=nb_opt-index
        l.append(score)
    list_pref_cote_des.append(l)

#print(pref_cote_opt)
#print(pref_cote_des)
#print(list_pref_cote_opt, list_pref_cote_des)
nbvar=nb_opt*nb_des
#1. somme sur j, xij<=1 un homme au plus une femme
#2. somme sur i, xij<=1 une femme au plus une femme
#3. stabilite
#4. xij egal a zero ou 1 (deux contraintes par variable)
nbcont = nb_des+nb_opt + nbvar*3

a = []


# 1. contraintes sur un homme
for i in range(nb_opt):
    vecteur=[0]*nbvar
    for j in range(nb_des):
        vecteur[ (i*nb_des) + j]=1
    a.append(vecteur)
# 2. contraintes sur une femme
for i in range(nb_des):
    vecteur=[0]*nbvar
    for j in range(nb_opt):
        vecteur[ (j*nb_des) + i]=1
    a.append(vecteur)
# 3. stabilite xij + nb(prek>prej) +nb(prel>prfi)
for i in range(nbvar):
    vecteur=[0]*nbvar
    vecteur[i]=1
    #homme correspond:
    index_homme=(i)//len(female)
    index_femme=i-index_homme*len(female)
    #print(index_homme,index_femme)
    v_pref_m_f=list_pref_cote_opt[index_homme][index_femme]
    v_pref_f_m=list_pref_cote_des[index_femme][index_homme]
    for k in range(nb_des):
        if list_pref_cote_opt[index_homme][k]>v_pref_m_f:
            vecteur[index_homme*len(female)+k]=1
    for l in range(nb_opt):
        if list_pref_cote_des[index_femme][l]>v_pref_f_m:
            vecteur[len(female)*l+index_femme]=1
    #print(vecteur,i,index_homme,index_femme)
    print(vecteur)
    a.append(vecteur)

#4.1 xij inf ou egal a 1
for i in range(nbvar):
    vecteur=[0]*nbvar
    vecteur[i]=1
    a.append(vecteur)
#4.2 xij sup ou egal a 0
    vecteur=[0]*nbvar
    vecteur[i]=1
    a.append(vecteur)

b=[1]*(nb_opt+nb_des+2*nbvar)
#for i in range(nb_opt+nb_des+2*nbvar)
for i in range(nbvar):
    b.append(0)

c=[]
# Ici on defini vij comme somme des preferences
for i in range(nb_opt):
    for j in range(nb_des):
        somme_pf=list_pref_cote_opt[i][j]+list_pref_cote_des[j][i]
        c.append(somme_pf)


lignes = range(nbcont)
colonnes = range(nbvar)
#print(b)
#print(c)
#print("hi")
#print(list_pref_cote_opt,list_pref_cote_des)
m = Model("mogplex")

# declaration variables de decision
x = []
for i in colonnes:
    x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]

# definition de l'objectif
m.setObjective(obj,GRB.MAXIMIZE)

# Definition des contraintes

for i in lignes:

    if i < nb_opt+nb_des:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
    else:
        if i <nb_opt+nb_des+nbvar:
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) >= b[i], "Contrainte%d" % i)
        else:
            if i <nb_opt+nb_des+ 2*nbvar:
                m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
            else:
                m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) >= b[i], "Contrainte%d" % i)
# Resolution
m.optimize()


print("")
print('Solution optimale:')
for j in colonnes:
    print('x%d'%(j+1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)
