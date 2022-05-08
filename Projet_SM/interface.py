import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from copy import deepcopy
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from sm import *
from algo3 import *
from algo4 import *
import os
import random
import time

IMPORT_DATA=0



def reproduce_pref(female,male,s_f,s_m,dim1,dim2):
    new_female=female[:dim1]
    new_male=male[:dim2]
    dic_male=dict()
    dic_female=dict()
    # two loops to generate two dictionnaries
    for i in new_male:
        lm=[fm for fm in s_m[i][1] if fm in new_female]
        dic_male[i]=['Single',lm]
    for j in new_female:
        lf=[ml for ml in s_f[j][1] if ml in new_male]
        dic_female[j]=['Single',lf]
    return new_female,new_male,dic_female,dic_male

class GaleShapleyCalculator:
    @staticmethod
    def cal_gs(dim1,dim2,opt1):
        print("!!!!!!!")
        global IMPORT_DATA
        global DATA
        print(IMPORT_DATA)
        if IMPORT_DATA==1:
            male,female,s_m,s_f=DATA
            female,male,s_f,s_m=reproduce_pref(female,male,s_f,s_m,dim1,dim2)
        else:
            female,male,s_f,s_m=gennere_set_f_m(dim1,dim2)
        print("======================")
        print("female preference",s_f)
        print("----------------------")
        print("male preference",s_m)
        print("======================")
        print("Stable couples")
        return Gale_Shapley(female,male,s_f,s_m, opt=opt1)


def compare_algo(size_K,size_S):
    global IMPORT_DATA
    global DATA
    lt1,lt2,lt3,lt4=[],[],[],[]
    lv1,lv2,lv3,lv4=[],[],[],[]

    nb_for_generation=5
    for i in range(5,(size_S+1)):
        K=[i]*i
        S=[j for j in range(1,i+1)]

        t=[0]*4
        sl1, sl2, sl3 ,sl4 = [], [], [], []
        import sys
        save_stdout = sys.stdout
        sys.stdout = open('trash', 'w')
        for j in range(nb_for_generation):
            if IMPORT_DATA==1:
                male,female,s_m,s_f=DATA
                female,male,s_f,s_m=reproduce_pref(female,male,s_f,s_m,i,i)
            else:
                female,male,s_f,s_m=gennere_set_f_m(i,i)
            ins=genere_instance(K,S, male, female, s_m, s_f)
            start = time.time()
            res1=calcul_difference_entre_gen(algo_1(deepcopy(ins)))
            stop = time.time()
            t[0]+=stop-start
            start = time.time()
            res2=calcul_difference_entre_gen(algo_2(deepcopy(ins)))
            stop = time.time()
            t[1]+=stop-start
            start = time.time()
            res3=calcul_difference_entre_gen(algo_3(deepcopy(ins)))
            stop = time.time()
            t[2]+=stop-start
            start = time.time()
            res4=prog_lineaire_advance(deepcopy(ins))
            stop = time.time()
            t[3]+=stop-start
            sl1.append(res1)
            sl2.append(res2)
            sl3.append(res3)
            sl4.append(res4)
            if res4>res3:
                print("!!!!!!!!!!!!!!!!!Erreur!!!!!!!!!!!!!!!!!")
        sys.stdout = save_stdout
        print("i==",i)
        lv1.append(sl1)
        lv2.append(sl2)
        lv3.append(sl3)
        lv4.append(sl4)
        lt1.append(np.mean(t[0]))
        lt2.append(np.mean(t[1]))
        lt3.append(np.mean(t[2]))
        lt4.append(np.mean(t[3]))
    Lg=[i for i in range(5,(size_S+1))]
    plt.plot(Lg,lt1, label="algo1")
    plt.plot(Lg,lt2, label="algo2")
    plt.plot(Lg,lt3, label="algo3")
    plt.plot(Lg,lt4, label="algo4")
    plt.title("Time comparation")
    plt.legend()
    plt.show()
    plt.plot(Lg,np.mean(lv1,axis=1), label="algo1")
    plt.plot(Lg,np.mean(lv2,axis=1), label="algo2")
    plt.plot(Lg,np.mean(lv3,axis=1), label="algo3")
    plt.plot(Lg,np.mean(lv4,axis=1), label="algo4")
    plt.title("Value comparation")
    plt.legend()
    plt.show()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Stable Mariage Calculator')
        self.geometry('600x200')
        self.resizable(0, 0)

        #female,male,s_f,s_m=gennere_set_f_m(dim1,dim2)
class CalculatorFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        def select_file():
            global IMPORT_DATA
            global DATA
            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            )

            filename = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)

            IMPORT_DATA=1
            DATA=lire_entree(filename)
            #text.insert('1.0', f.readlines())
            """showinfo(
                title='Selected File',
                message=filename
            )"""

        def reset_file():
            global IMPORT_DATA
            IMPORT_DATA=0
        # open button
        open_button = ttk.Button(
            self,
            text='Open a File',
            command=select_file
        ).grid(column=0, row=0)
        reset_button = ttk.Button(
            self,
            text='Reset',
            command=reset_file
        ).grid(column=1, row=0)

        self.first_label = ttk.Label(self, text='Simple SM Problem').grid(column=0, row=1, sticky=tk.W)


        self.male_label = ttk.Label(self, text='Nb male')
        self.male_label.grid(column=1, row=2, sticky=tk.W)



        self.nb_male = tk.StringVar()
        self.nb_male_entry = ttk.Entry(self, textvariable=self.nb_male,width=5)
        self.nb_male_entry.grid(column=2, row=2)
        self.nb_male_entry.focus()

        self.female_label = ttk.Label(self, text='Nb female')
        self.female_label.grid(column=3, row=2, sticky=tk.W)

        self.nb_female = tk.StringVar()
        self.nb_female_entry = ttk.Entry(self, textvariable=self.nb_female,width=5)
        self.nb_female_entry.grid(column=4, row=2)
        self.nb_female_entry.focus()

        male_case, female_case = tk.StringVar(), tk.StringVar()

        opt_side=tk.StringVar()
        male_case_check = ttk.Radiobutton(
            self,
            text='Male optimal',
            value="male",
            variable=opt_side)
        male_case_check.grid(column=1, row=3, sticky=tk.W)

        female_case_check = ttk.Radiobutton(
            self,
            text='Female optimal',
            value="female",
            variable=opt_side)
        female_case_check.grid(column=3, row=3, sticky=tk.W)
        dic_side={"female":0,"male":1}

        calculate_button=ttk.Button(self, text='Calculate',command=lambda:print(GaleShapleyCalculator.cal_gs(int(self.nb_male.get()), int(self.nb_female.get()),dic_side[opt_side.get()])) ,width=7).grid(column=5, row=3)

        self.second_label = ttk.Label(self, text='Sequence SM Problem').grid(column=0, row=4, sticky=tk.W)

        self.value = ttk.Label(self, text='Max nomber').grid(column=1, row=5, sticky=tk.W)

        self.max_nomber = tk.StringVar()
        self.max_nomber_entry = ttk.Entry(self, textvariable=self.max_nomber,width=5)
        self.max_nomber_entry.grid(column=2, row=5)
        self.max_nomber_entry.focus()

        male_case, female_case = tk.StringVar(), tk.StringVar()

        opt_side=tk.StringVar()
        male_case_check = ttk.Radiobutton(
            self,
            text='Male optimal',
            value="male",
            variable=opt_side)
        male_case_check.grid(column=1, row=3, sticky=tk.W)

        female_case_check = ttk.Radiobutton(
            self,
            text='Female optimal',
            value="female",
            variable=opt_side)
        female_case_check.grid(column=3, row=3, sticky=tk.W)
        dic_side={"female":0,"male":1}

        self.first_label = ttk.Label(self, text='(MaxValue>5)').grid(column=3, row=5, sticky=tk.W)
        compare_button=ttk.Button(self, text='Compare',command=lambda:compare_algo(int(self.max_nomber.get()), int(self.max_nomber.get())) ,width=7).grid(column=5, row=5)

        self.grid(padx=10, pady=10, sticky=tk.NSEW)

if __name__ == "__main__":
    app = App()
    CalculatorFrame(app)
    app.mainloop()
