from gurobipy import *
from sm import gennere_set_f_m
female,male,s_f,s_m=gennere_set_f_m(17,20)
cote_optimal=male
pref_cote_opt=s_m
cote_dessimale=female
pref_cote_des=s_f


nb_opt=len(cote_optimal)
nb_des=len(cote_dessimale)
print(nb_opt,nb_des)
# Creation la liste de preference
#print(cote_dessimale)
list_pref_cote_opt=[]
list_pref_cote_des=[]
for i in range(nb_opt):
    l=[]
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

nbvar=nb_opt*nb_des
#1. somme sur j, xij<=1 un homme au plus une femme
#2. somme sur i, xij<=1 une femme au plus une femme
#3. stabilite
#4. xij egal a zero ou 1 (deux contraintes par variable)
nbcont = nb_des+nb_opt + nbvar*3



c=[]
# Ici on defini vij comme somme des preferences
for i in range(nb_opt):
    for j in range(nb_des):
        somme_pf=list_pref_cote_opt[i][j]+list_pref_cote_des[j][i]
        c.append(somme_pf)

lignes = range(nbcont)
colonnes = range(nbvar)
m = Model("mogplex")

# declaration variables de decision
x = []
for i in colonnes:
    x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d" % (i+1)))

m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]

# definition de l'objectif
m.setObjective(obj,GRB.MAXIMIZE)

for i in range(nb_opt):
    print([y+nb_des*i for y in range(nb_des)])
    m.addConstr(quicksum(x[j] for j in [y+nb_des*i for y in range(nb_des)]) <= 1, "Contrainte%d" % i)
for i in range(nb_des):
    print([y*nb_des+i for y in range(nb_opt)])
    m.addConstr(quicksum(x[j] for j in [y*nb_des+i for y in range(nb_opt)]) <= 1, "Contrainte%d" % i)
for i in range(nbvar):
    index_var=[i]
    index_homme=(i)//len(female)
    index_femme=i-index_homme*len(female)
    v_pref_m_f=list_pref_cote_opt[index_homme][index_femme]
    v_pref_f_m=list_pref_cote_des[index_femme][index_homme]
    for k in range(nb_des):
        if list_pref_cote_opt[index_homme][k]>v_pref_m_f:
            index_var.append(index_homme*len(female)+k)
    for l in range(nb_opt):
        if list_pref_cote_des[index_femme][l]>v_pref_f_m:
            index_var.append(len(female)*l+index_femme)
    index_var=list(set(index_var))
    print(index_var)
    m.addConstr(quicksum(x[j] for j in index_var) >= 1, "Contrainte%d" % i)
for i in range(nbvar):
    m.addConstr(x[i]  >= 0, "Contrainte%d" % i)
    m.addConstr(x[i]  <= 1, "Contrainte%d" % i)
# maj du modele pour integrer les nouvelles variables
m.optimize()


print("")
print('Solution optimale:')
for j in colonnes:
    print('x%d'%(j+1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)
