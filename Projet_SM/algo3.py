from gurobipy import *
from gs import Gale_Shapley
import pandas as pd
def prog_lineaire(list_instance):
    """
    :param :list_instance : list of qua-tuplets contaning
        - male_i/female_i : list of males/females for t=i
        - pm_i/pf_i : dictionary of preference for t=i
    Principe de l'algo:
    #Methode: PL
    #Variable:
        - x_{ij}^{t} -> variable xij a l'instant t
    #Valeur de variable:
        - 1 si xij forme une couple a l'instant t
        - 0 sinon
    #Fonction objective:
        Max save all couples
    #Contraintes:
        - pour tout t, sum xij sur i ou j soit inf a 1 (mariage)
        - xijt>=0
        - xijt<=1
        - stabilite

    :return : list of couples of different generations
    """
    mariage=[]
    male_i,female_i,pm_i, pf_i=list_instance[0]

    # The first generation is genarated by Gale_Shapley
    mariage_avant=Gale_Shapley(male_i,female_i,pm_i,pf_i)
    mariage.append(mariage_avant)


    # Creation la liste de preference
    for nb in range(1,len(list_instance)):

        male_i,female_i,pm_i, pf_i=list_instance[nb]

        nb_m=len(male_i)
        nb_f=len(female_i)

        matrix_mariage=[]

        #Generate vecteur_mariage
        for i in range(len(male_i)):
            sous_matrix=[]
            for j in range(len(female_i)):
                if (male_i[i],female_i[j]) in mariage_avant:
                    #print(male_i[j],female_i[k])
                    sous_matrix.append(1)
                else:
                    sous_matrix.append(0)
            matrix_mariage.append(sous_matrix)
        #print("matrix_mariage",matrix_mariage)
        #print("here",mariage_avant)
        #nbvar=nb_m*nb_f#nb_m*nb_f
        #1. somme sur j, xij<=1 un homme au plus une femme
        #2. somme sur i, xij<=1 une femme au plus un homme
        #3. stabilite
        #4. xij egal a zero ou 1 (deux contraintes par variable)
        #nbcont = nb_f+nb_m + nbvar*3 #+2 +nbvar


        m = Model("mogplex")

        # declaration variables de decision
        x = []
        for i in range(nb_m):
            sous_list=[]
            for j in range(nb_f):
                sous_list.append(m.addVar(vtype=GRB.BINARY, lb=0, name=f"x{i+1:d}{j+1:d}"))
            x.append(sous_list)

        m.update()
        obj = LinExpr();
        obj =0

        c=matrix_mariage

        for i in range(nb_m):
            for j in range(nb_f):
                obj += c[i][j] * x[i][j]

        # definition de l'objectif
        m.setObjective(obj,GRB.MAXIMIZE)

        counter=0
        for i in range(nb_m):
            m.addConstr(quicksum(x[i][j] for j in [y for y in range(nb_f)]) <= 1, "Contrainte%d" % counter)
            counter+=1
        for j in range(nb_f):
            m.addConstr(quicksum(x[i][j] for i in [y for y in range(nb_m)]) <= 1, "Contrainte%d" % counter)
            counter+=1
        for i in range(nb_m):
            for j in range(nb_f):
                m.addConstr(x[i][j]  >= 0, "Contrainte%d" % counter)
                m.addConstr(x[i][j]  <= 1, "Contrainte%d" % (counter+1) )
                counter+=2
        for i in range(len(male_i)):
            for j in range(len(female_i)):
                list_index=[(i,j)]
                #check=[(i,j)]
                homme=male_i[i]
                femme=female_i[j]
                v_pref_m_f=pm_i[homme][1].index(femme)
                v_pref_f_m=pf_i[femme][1].index(homme)

                for k in range(len(male_i)):
                    new_homme=male_i[k]
                    #print("indice",pf_i[femme][1].index(new_homme),v_pref_f_m, new_homme, homme,k,i)
                    if pf_i[femme][1].index(new_homme)<v_pref_f_m:
                        list_index.append( (k, j) )
                    """
                    if pf_i[femme][1].index(new_homme)<=v_pref_f_m:
                        print(pf_i[femme][1])
                        print("indice",pf_i[femme][1].index(new_homme),v_pref_f_m, new_homme, homme, k, j, i, j)
                        check.append( (k, j) )
                    print("=======male======")
                    print(list(set(list_index)))
                    print(list(set(check)))"""
                for l in range(len(female_i)):
                    new_femme=female_i[l]
                    #print("indice",pm_i[homme][1].index(new_femme),v_pref_m_f, new_femme, femme)
                    if pm_i[homme][1].index(new_femme)<v_pref_m_f:
                        list_index.append( (i, l) )
                    """
                    if pm_i[homme][1].index(new_femme)<=v_pref_m_f:
                        print(pm_i[homme][1])
                        print("indice",pm_i[homme][1].index(new_femme),v_pref_m_f, new_femme, femme, i, l, i, j)
                        check.append( (i, l) )
                    print("=======female======")
                    print(list(set(list_index)))
                    print(list(set(check)))"""

                list_index=list(set(list_index))
                #check=list(set(check))
                #print("list_index",list_index)
                #print("check", check)
                m.addConstr(quicksum(x[m][n] for m,n in list_index) >= 1, "Contrainte%d" % counter)
                counter+=1
        import sys
        save_stdout = sys.stdout
        sys.stdout = open('trash', 'w')
        m.optimize()
        sys.stdout = save_stdout
        render=0

        if render==1:
            status = m.status
            varInfo = [(v.varName, v.LB, v.UB) for v in m.getVars() ] # use list comprehension
            df_var = pd.DataFrame(varInfo) # convert to pandas dataframe
            df_var.columns=['Variable Name','LB','UB'] # Add column headers
            print(df_var.head())

            # Linear constraint info
            constrInfo = [(c.constrName, m.getRow(c), c.Sense, c.RHS) for c in m.getConstrs() ]
            df_constr = pd.DataFrame(constrInfo)
            df_constr.columns=['Constraint Name','Constraint equation', 'Sense','RHS']
            print(df_constr.head())
            print(m.display())



        #

        ma=[]
        #generation of couples
        for i in range(len(male_i)):
            for j in range(len(female_i)):
                if x[i][j].x==1:
                    ma.append( (male_i[i],female_i[j]) )
        #print("fin",ma)
        mariage_avant=ma
        mariage.append(ma)
        #print('Valeur de la fonction objectif :', m.objVal)
    return mariage
