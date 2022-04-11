def Gale_Shapley(female,male,pref_f,pref_m,optimal=0):
    if optimal==0:
        side_opt=female.copy()
        pref_opt=pref_f
        side_des=male.copy()
        pref_des=pref_m
    else:
        side_opt=male.copy()
        pref_opt=pref_m
        side_des=female.copy()
        pref_des=pref_f
    #print("here")
    #print(side_opt)
    while side_opt:
        #print(pref_des)
        person=side_opt.pop()
        #print("hi")
        #print(pref_opt)
        for person_partner in (pref_opt[person][1]):
            #print(person_partner)
            print(pref_des[person_partner])
            if pref_des[person_partner][0]=="Single":
                print("hi", person,"\n")
                pref_opt[person][0]=person_partner
                pref_des[person_partner][0]=person
                pref_opt[person][0]=person_partner
                #person=side_opt.pop(0)
                break
            else:
                #print(person)
                #print(pref_des[person_partner][0],"here\n")
                competitor=pref_des[person_partner][0]
                pref_comp=pref_des[person_partner][1].index(competitor)
                pref_person=pref_des[person_partner][1].index(person)
                if pref_person<pref_comp:
                    print("here")
                    pref_des[person_partner][0]=person
                    pref_opt[person][0]=person_partner
                    pref_opt[competitor][0]="Single"
                    side_opt.append(competitor)
                    #person=side_opt.pop(0)
                    break
            print(pref_opt,"\n")
            print(pref_des,"\n")
    return [(x, y[0])  for x,y in pref_opt.items() if y[0]!='Single']
