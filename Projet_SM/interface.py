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
from os import path
import random
import time

global IMPORT_DATA
IMPORT_DATA=0
def save_result(female,male,s_f,s_m,couples,filename):
    if path.exists(filename):
        top= tk.Toplevel()
        top.geometry("450x150")
        top.title("File name erreur")
        tk.Label(top, text= "File already exists, please change the file name!", font=('Mistral 12 bold')).place(x=100,y=70)
        return 0
    with open('./'+filename,'w') as f:
        f.write('name1\n\t')
        f.write(str(female))
        f.write('\nname2\n\t')
        f.write(str(male))
        f.write('\npref1\n\t')
        f.write(str(s_f))
        f.write('\npref2\n\t')
        f.write(str(s_m)+'\n')
        f.write("couples\n\t")
        for x,y in couples:
            f.write('\t'+x+' '+y+'\n')


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
    def cal_gs(dim1,dim2,opt1,var_check_save,filename):
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
        result=Gale_Shapley(female,male,s_f,s_m, opt=opt1)
        if var_check_save==1:
            save_result(female,male,s_f,s_m,result,filename)
        return result


def compare_algo(minv,maxv,step,var_check_save,filename,var_check_plot,filenameplot):#size_K,size_S):
    print(filenameplot)
    if minv<=1 or maxv<=minv:
        top= tk.Toplevel()
        top.geometry("450x150")
        top.title("Value erreur")
        tk.Label(top, text= "Min value >= 2 and Min value < Max value!", font=('Mistral 12 bold')).place(x=100,y=70)
        return 0
    dir=filename
    dir=dir.replace("data.txt",'')
    if dir =='':
        dir=filenameplot
        dir=dir.replace("plot.png",'')
    if path.exists(filename) or path.exists(filenameplot) or path.exists(dir):
        top= tk.Toplevel()
        top.geometry("450x150")
        top.title("File name erreur")
        tk.Label(top, text= "File already exists, please change the file name!", font=('Mistral 12 bold')).place(x=100,y=70)
        return 0
    if var_check_save==1:
        os.mkdir(dir)
    
    global IMPORT_DATA
    global DATA
    #global stop
    lt1,lt2,lt3,lt4=[],[],[],[]
    lv1,lv2,lv3,lv4=[],[],[],[]

    nb_for_generation=5
    if var_check_save==1:
        f=open(filename,'w')
    for i in range(minv,maxv+1,step):
        K=[i]*i
        S=[j for j in range(1,i+1)]
        print(K,S)
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
            m1=algo_1(deepcopy(ins))
            res1=calcul_difference_entre_gen(m1)
            stop = time.time()
            t[0]+=stop-start
            start = time.time()
            m2=algo_2(deepcopy(ins))
            res2=calcul_difference_entre_gen(m2)
            stop = time.time()
            t[1]+=stop-start
            start = time.time()
            m3=algo_3(deepcopy(ins))
            res3=calcul_difference_entre_gen(m3)
            stop = time.time()
            t[2]+=stop-start
            start = time.time()
            res4,m4=prog_lineaire_advance(deepcopy(ins))
            stop = time.time()
            t[3]+=stop-start
            """if stop==1:
                change_stop()
                exit()"""
            sl1.append(res1)
            sl2.append(res2)
            sl3.append(res3)
            sl4.append(res4)
            if var_check_save==1:
                f.write("Value: "+str(i)+" Iteration:"+str(j)+"\n")
                f.write('name1\n\t')
                f.write(str(female))
                f.write('\nname2\n\t')
                f.write(str(male))
                f.write('\npref1\n\t')
                f.write(str(s_f))
                f.write('\npref2\n\t')
                f.write(str(s_m)+'\n')
                f.write('\nalgo1\n\t')
                f.write(str(m1))
                f.write('\nalgo2\n\t')
                f.write(str(m2))
                f.write('\nalgo3\n\t')
                f.write(str(m3))
                f.write('\nalgo4\n\t')
                f.write(str(m4))
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
    Lg=[i for i in range(minv,(maxv+1))]
    plt.plot(Lg,lt1, label="algo1")
    plt.plot(Lg,lt2, label="algo2")
    plt.plot(Lg,lt3, label="algo3")
    plt.plot(Lg,lt4, label="algo4")
    plt.legend()
    if var_check_plot==1:
        plt.savefig(filenameplot)
    plt.show()
    plt.plot(Lg,np.mean(lv1,axis=1), label="algo1")
    plt.plot(Lg,np.mean(lv2,axis=1), label="algo2")
    plt.plot(Lg,np.mean(lv3,axis=1), label="algo3")
    plt.plot(Lg,np.mean(lv4,axis=1), label="algo4")
    plt.legend()
    if var_check_plot==1:
        filenameplot=filenameplot.replace(".png","1.png")
        print(filenameplot)
        plt.savefig(filenameplot)
    plt.show()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Stable Mariage Calculator')
        self.geometry('600x300')
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


        save_filename=tk.StringVar()

        #file_label = ttk.Label(self, text='File name')
        #file_label.grid(column=3, row=4, sticky=tk.W)
        save_filename_entry=ttk.Entry(self, textvariable=save_filename,width=15)
        save_filename_entry.grid(column=2, row=4,columnspan = 3)
        save_filename_entry.configure(state='disabled')
        save_filename_entry.focus()
        var_check_save = tk.IntVar()

        from datetime import datetime

        def naccheck( entry, var):
            if var.get() == 0:
                entry.delete(0, tk.END)
                entry.configure(state='disabled')

            else:
                entry.configure(state='normal')
                now = datetime.now().strftime("./data/%d_%m_%Y_%H_%M_%S_stable_mariage.txt")
                entry.insert(0,now)
        check_save=ttk.Checkbutton(self,text='Save as file',variable=var_check_save,command=lambda e=save_filename_entry,v=var_check_save: naccheck(e,v)).grid(column=1, row=4)

        calculate_button=ttk.Button(self, text='Calculate',command=lambda:print(GaleShapleyCalculator.cal_gs(int(self.nb_female.get()),int(self.nb_male.get()),dic_side[opt_side.get()],var_check_save.get(),save_filename_entry.get())) ,width=7).grid(column=5, row=4)

        self.second_label = ttk.Label(self, text='Sequence SM Problem').grid(column=0, row=5, sticky=tk.W)

        self.minvalue = ttk.Label(self, text='Min value').grid(column=1, row=6, sticky=tk.W)
        self.min_nomber = tk.StringVar()
        self.min_nomber_entry = ttk.Entry(self, textvariable=self.min_nomber,width=5)
        self.min_nomber_entry.grid(column=2, row=6)
        self.min_nomber_entry.focus()

        minvalsa2 = ttk.Label(self, text='(Min value >= 2 and Min value < Max value)').grid(column=3, row=6, sticky=tk.W,columnspan = 3)


        self.maxvalue = ttk.Label(self, text='Max value').grid(column=1, row=7, sticky=tk.W)

        self.max_nomber = tk.StringVar()
        self.max_nomber_entry = ttk.Entry(self, textvariable=self.max_nomber,width=5)
        self.max_nomber_entry.grid(column=2, row=7)
        self.max_nomber_entry.focus()

        self.setpvalue = ttk.Label(self, text='Step').grid(column=3, row=7, sticky=tk.W)
        self.step_nomber = tk.StringVar()
        self.step_nomber_entry = ttk.Entry(self, textvariable=self.step_nomber,width=5)
        #self.step_nomber_entry.insert(0,1)
        self.step_nomber_entry.grid(column=4, row=7)
        self.step_nomber_entry.focus()


        def naccheck2( entry, var,entry1,type):
            format={1:'data.txt',-1:'plot.png'}
            if var.get() == 0:
                entry.delete(0, tk.END)
                entry.configure(state='disabled')

            else:

                entry.configure(state='normal')
                if entry1.get()!='':
                    print(entry1.get())
                    now = entry1.get().replace(format[-type],format[type])
                else:
                    now = datetime.now().strftime("./data/%d_%m_%Y_%H_%M_%S_stable_mariage/"+format[type])
                print(now)
                entry.insert(0,now)

        save_filename1=tk.StringVar()

        #file_label = ttk.Label(self, text='File name')
        #file_label.grid(column=3, row=4, sticky=tk.W)
        save_filename1_entry=ttk.Entry(self, textvariable=save_filename1,width=15)
        save_filename1_entry.grid(column=2, row=8,columnspan = 3)
        save_filename1_entry.configure(state='disabled')
        save_filename1_entry.focus()
        var_check_save1 = tk.IntVar()

        save_plot=tk.StringVar()


        save_plot_entry=ttk.Entry(self, textvariable=save_plot,width=15)
        save_plot_entry.grid(column=2, row=9,columnspan = 3)
        save_plot_entry.configure(state='disabled')
        save_plot_entry.focus()
        check_save1=ttk.Checkbutton(self,text='Save as file',variable=var_check_save1,command=lambda e=save_filename1_entry,v=var_check_save1,e1=save_plot_entry: naccheck2(e,v,e1,1)).grid(column=1, row=8)




        var_check_plot = tk.IntVar()

        check_plot=ttk.Checkbutton(self,text='Save plots',variable=var_check_plot,command=lambda e=save_plot_entry,v=var_check_plot, e1=save_filename1_entry: naccheck2(e,v,e1,-1)).grid(column=1, row=9)

        """def change_stop():
            global stop
            if stop==1:
                stop=0
            else:
                stop=1
        stop_button=tk.Button(self, text='Stop',command=lambda: change_stop()).grid(column=3, row=9,columnspan = 2)"""

        compare_button=tk.Button(self, text='Compare',command=lambda:compare_algo(int(self.min_nomber.get()), int(self.max_nomber.get()), int(self.step_nomber.get()),var_check_save1.get(),save_filename1_entry.get(),var_check_plot.get(),save_plot_entry.get()) ,width=7).grid(column=5, row=9)

        self.grid(padx=10, pady=10, sticky=tk.NSEW)

if __name__ == "__main__":
    app = App()
    CalculatorFrame(app)
    app.mainloop()
