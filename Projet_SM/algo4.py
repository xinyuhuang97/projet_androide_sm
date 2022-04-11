"""
Principe de l'algo:
#Methode: PL
#Variable:
    - x_{ij}^{t} -> variable xij a l'instant t
    - z_{ij}^{t} valeur a minimiser
#Valeur de variable:
    - 1 si xij forme une couple a l'instant t
    - 0 sinon
#Fonction objective:
    Min sum zijt
#Contraintes:
    - pour tout t, sum xij sur i ou j soit inf a 1 (mariage)
    - zijt>=xijt - xij{t-1}
    - zijt>=0
    - xijt>=0
    - xijt<=1
#Advantage:
    -Comparer a l'algo iterative, resoudre le problem en une seule iteration
    -Resoudre le problem de facon gloable qui minimise la difference gloable
"""
from gs import Gale_Shapley
from gurobipy import *

def prog_lineaire_advance(list_instance):
    nb_m=0
    nb_f=0
    list_m=[]
    list_f=[]
    duree_t=0
    for instance_t in list_instance:
        print(instance_t)
        a,b,_,_=instance_t
        lg_a=len(a)
        lg_b=len(b)
        duree_t+=1
        if lg_a>nb_m:
            list_m=a
            nb_m=lg_a
        if lg_b>nb_f:
            list_f=b
            nb_f=lg_b


    male_i,female_i,pm_i, pf_i=list_instance[0]
    mariage_avant=Gale_Shapley(male_i,female_i,pm_i,pf_i)

    matrix_mariage=[]
    for j in range(nb_m):
        sous_matrix=[]
        for k in range(nb_f):
            if (list_m[j],list_f[k]) in mariage_avant:
                print(male_i[j],female_i[k])
                sous_matrix.append(1)
            else:
                sous_matrix.append(0)
        matrix_mariage.append(sous_matrix)
    #
    nbvar=nb_m*nb_f*(duree_t-1)*2
    nbcont=nb_m*duree_t + nb_f*duree_t + nb_m*nb_f*(duree_t-1)*2 +nb_m*nb_f*duree_t


    lignes = range(nbcont)
    colonnes = range(nbvar)
    m = Model("mogplex")

    # declaration variables de decision
    x = []
    for nn in ([0,1]):
        for i in range(nb_m):
            sous_list=[]
            for j in range(nb_f):
                ss_list=[]
                for k in range(duree_t-1):
                    ss_list.append(m.addVar(vtype=GRB.BINARY, lb=0, name=f"x{i+1:d}{j+1:d}{k+1:d}" ))
                sous_list.append(ss_list)
            x.append(sous_list)
    print(len(x),len(x[0]),len(x[0][0]))

    m.update()

    obj = LinExpr();
    obj =0


    c=[]
    for nn in ([0,1]):
        for i in range(nb_m):
            sous_list=[]
            for j in  range(nb_f):
                ss_list=[]
                for k in range(duree_t-1):
                    ss_list.append(nn)
                sous_list.append(ss_list)
            c.append(sous_list)


    for i in range(nb_m*2):
        for j in  range(nb_f):
            for k in range(duree_t-1):
                obj += c[i][j][k] * x[i][j][k]

    m.setObjective(obj,GRB.MINIMIZE)

    for t in range(duree_t-1):
        for i in range(nb_m):
            m.addConstr(quicksum(x[i][j][t] for j in [y for y in range(nb_f)]) <= 1, "Contrainte%d" % i)
    for t in range(duree_t-1):
        for j in range(nb_f):
            m.addConstr(quicksum(x[i][j][t] for i in [y for y in range(nb_m)]) <= 1, "Contrainte%d" % i)
    #1) Le cas initial
    for i in range(nb_m):
        for j in range(nb_f):
            m.addConstr(x[i+nb_m][j][0] >= x[i][j][0]-matrix_mariage[i][j], "Contrainte%d" % i)
    #2) Le cas general
    for i in range(nb_m):
        for j in range(nb_f):
            for t in range(1,duree_t-1):
                m.addConstr(x[i+nb_m][j][t] >= x[i][j][t]-x[i][j][t-1], "Contrainte%d" % i)
    for i in range(nb_m):
        for j in range(nb_f):
            for t in range(duree_t-1):
                m.addConstr(x[i][j][t] >= 0, "Contrainte%d" % i)
                m.addConstr(x[i][j][t] <= 1, "Contrainte%d" % i)
                m.addConstr(x[i+nb_m][j][t] >= 0, "Contrainte%d" % i)
    for t in range(duree_t-1):
        a,b,_,_=list_instance[t]
        valmin=min(len(a),len(b))
        print(valmin)
        m.addConstr(quicksum(x[i][j][t] for i in [x for x in range(nb_m)] for j in [ y for y in range(nb_f)] ) <=valmin, "Contrainte%d" % i)
        m.addConstr(quicksum(x[i][j][t] for i in [x for x in range(nb_m)] for j in [ y for y in range(nb_f)] ) >=valmin, "Contrainte%d" % i)

    m.optimize()



    print("")
    print('Solution optimale:')
    for nn in ([0,1]):
        for i in range(nb_m):
            for j in range(nb_f):
                for k in range(duree_t-1):
                    print(f"x{i+1+nn*nb_m:d}_{j+1:d}_{k+1:d}", '=', x[nn*nb_m+i][j][k].x)
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
    couple=[]
    for k in range(duree_t-1):
        couple_k=[]
        for i in range(nb_m):
            for j in range(nb_f):
                if x[i][j][k].x==1:
                    couple_k.append((list_m[i],list_f[j]))
        couple.append(couple_k)
    print(couple)
    return int(m.objVal)
