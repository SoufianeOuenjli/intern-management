from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import json
import re

# =============== Class pour Verifier les inputes ===============
class Verifier:
    def __init__(self,type,parent,format, exemple):
        self.type = type
        self.parent = parent
        self.format = format
        self.exemple = exemple
    def verifier_format(self,text):
        self.verif = re.match(self.format, text)
        if self.verif != None:
            return True
        else:
            message = f"Le format du champ {self.type} est invalide!\nExemple : {self.exemple}"
            tkinter.messagebox.showwarning("Attention", message, parent=self.parent)
            return False


# =============== Pgrame Principale ===============

modules = []
cnid = []
tuples = []

app = tk.Tk()
app.geometry('780x480')
app.resizable(0,0)

app.title("Gestion Stagiaire")
icon = PhotoImage(file="logo.png")
app.iconphoto(True, icon)
message = tk.Label(app, text="Gestion Stagiaire" )

#=============== Chargement des données ===============
try:
    with open("Stagiare.json", "r") as f:
        data = json.load(f)
except:
    with open("Stagiare.json", "w") as f:
        d = []
        f.write(json.dumps(d))
        data = json.load(f)

#=============== Convertie un dictionnaire a un tuple ===============
def convert_to_tuples(data):
    for trainee in data:
        cni = trainee.get("Cni", "")
        nom = trainee.get("Nom", "")
        prenom = trainee.get("Prenom", "")
        age = trainee.get("Age", "")
        email = trainee.get("Email", "")
        note = trainee.get("Note", "{}")

        trainee_tuple = (cni, nom, prenom, age, email, note)
        tuples.append(trainee_tuple)
    return tuples
trainee_tuples = convert_to_tuples(data)

#=============== Style de TK ===============
style = ttk.Style()
style.theme_use('clam')
style.map('W.TButton',
                foreground=[('pressed', 'white'), ('active', 'red')],
                background=[('pressed', 'red'), ('active', 'white')]
                )

#=============== Les bouttons ===============
ajout = ttk.Button(text='Ajouter stagiare' , width = 25)
sup = ttk.Button(text='Suprimer stagiare', style = 'W.TButton', width = 25)
mod = ttk.Button(text='Modifier stagiare', width = 25)
enre = ttk.Button(text='Enregistrer', width = 40)
a_module = ttk.Button(text='Ajouter Module', width = 25)
m_module = ttk.Button(text='Modifier Module', width = 25)
s_module = ttk.Button(text='Suprimer Module', style = 'W.TButton', width = 25)


area = ('CNE','Nom','Prenom','Age','Email')

tv=ttk.Treeview(app,columns=area,show='headings',height=7)
for i in range(5):
    if i == 4:
        tv.column(area[i],width=170,anchor=CENTER)
        tv.heading(area[i],text=area[i])
    else:
        tv.column(area[i], width=70, anchor=CENTER)
        tv.heading(area[i], text=area[i])

for i in range(len(data)):
    tv.insert('', 'end', values=trainee_tuples[i])

message.place(x=350, y=10)
tv.place(x=70, y=50)

ajout.place(x=550, y=50)
mod.place(x=550, y=120)
sup.place(x=550, y=186)
a_module.place(x=358, y=230)
m_module.place(x=358, y=278)
s_module.place(x=358, y=327)

enre.place(x=250, y=420)

n = ("Module", "note")
note_view = ttk.Treeview(app, columns=n, show='headings', height=5)
for i in range(2):
    note_view.column(n[i], width=130, anchor=CENTER)
    note_view.heading(n[i], text=n[i])
note_view.place(x=70,y=230)

# =============== Selectioner un Ligne ===============
def click_row(evt):
    global info
    modules = []
    nte = []
    curItem = tv.focus()
    value = tv.item(curItem)['values']
    try:
        for i in range(len(data) - 1, -1, -1):
            if data[i]['Cni'] == value[0]:
                info = data[i]

        for key, value in info['Note'].items():
            module = key
            Note = value
            ntuple = (module, Note)
            nte.append(ntuple)

        for item in note_view.get_children():
            note_view.delete(item)
        for i in range(len(nte)):
            note_view.insert("", "end", values=nte[i])
        modules.append(nte)
        cnid.insert(0,info)

    except BaseException as e:
        return e

# =============== Ajouter Stagiare ===============
def ajouter_stagiare(evt):
    ajouter = tk.Tk()
    ajouter.geometry('300x280')
    m = ttk.Label(ajouter, text="Ajouter Stagiaire")

    cne = ttk.Label(ajouter, text='Cne:')
    cne_saisie = ttk.Entry(ajouter)

    nom = ttk.Label(ajouter, text='Nom:')
    nom_saisie = ttk.Entry(ajouter)

    prenom = ttk.Label(ajouter, text='Prenom:')
    pre_saisie = ttk.Entry(ajouter)

    age = ttk.Label(ajouter, text='Age:')
    age_saisie = ttk.Entry(ajouter)

    email = ttk.Label(ajouter, text='Email:')
    email_saisie = ttk.Entry(ajouter)

    btn_ajout = ttk.Button(ajouter,text="Ajouter")

    m.pack()

    cne.place(x=50, y=40)
    cne_saisie.place(x=100, y=40)

    nom.place(x=50,y=70)
    nom_saisie.place(x=100,y=70)

    prenom.place(x=50, y=100)
    pre_saisie.place(x=100, y=100)

    age.place(x=50, y=130)
    age_saisie.place(x=100, y=130)

    email.place(x=50, y=160)
    email_saisie.place(x=100, y=160)

    btn_ajout.place(x = 120, y=210)

    # =============== Objets pour Verifier les inputes ===============
    verifier_cne = Verifier("Cne", ajouter, r"^[A-Z]+\d+$", "CD4532")
    verifier_nom = Verifier("Nom", ajouter, r"^[A-Z]{1}[a-z]+$", "Omari")
    verifier_prenom = Verifier("Prenom", ajouter, r"^[A-Z]{1}[a-z]+$", "Karim")
    verifier_age = Verifier("Age", ajouter, r"^\d{1,3}$","25")
    verifier_email = Verifier("Email", ajouter,r"^[\w\._\-]+@\w+\.[a-z]{3,4}$","exemple@gmail.com")

    def ajout_sta(evt):
        for i in range(len(data)-1,-1,-1):
            if data[i]['Cni'] == cne_saisie.get():
                message = "Cette CIN est deja existe"
                return tkinter.messagebox.showwarning("Attention", message, parent=ajouter)
            if data[i]['Email'] == email_saisie.get():
                message = "Cette Email est deja existe"
                return tkinter.messagebox.showwarning("Attention", message, parent=ajouter)
        if ( verifier_cne.verifier_format(cne_saisie.get()) and verifier_nom.verifier_format(nom_saisie.get()) and verifier_prenom.verifier_format(pre_saisie.get()) and verifier_age.verifier_format(age_saisie.get()) and verifier_email.verifier_format(email_saisie.get())):
            cn = cne_saisie.get()
            no = nom_saisie.get()
            pre = pre_saisie.get()
            ag = age_saisie.get()
            emai = email_saisie.get()

            stag = {'Cni': cn, 'Nom': no, 'Prenom': pre, 'Age': ag, 'Email': emai, 'Note': {}}

            stag2 = (cn, no, pre, ag, emai)

            data.append(stag)
            tv.insert('', 'end', values=stag2)
            print(emai)

    btn_ajout.bind("<Button-1>", ajout_sta)

# =============== Modufier Stagiare ===============
def modifier_stagiare(evt):
    if(len(cnid)>0):
        modifier = tk.Tk()
        modifier.geometry('300x280')

        m = ttk.Label(modifier, text="Modifier Stagiaire")

        cne = ttk.Label(modifier, text='Cne:')
        cne_saisie = ttk.Entry(modifier)
        cne_saisie.insert(0,f"{cnid[0]['Cni']}")
        cne_saisie.configure(state='disabled')

        nom = ttk.Label(modifier, text='Nom:')
        nom_saisie = ttk.Entry(modifier)
        nom_saisie.insert(0,f"{cnid[0]['Nom']}")

        prenom = ttk.Label(modifier, text='Prenom:')
        pre_saisie = ttk.Entry(modifier)
        pre_saisie.insert(0,f"{cnid[0]['Prenom']}")

        age = ttk.Label(modifier, text='Age:')
        age_saisie = ttk.Entry(modifier)
        age_saisie.insert(0,f"{cnid[0]['Age']}")

        email = ttk.Label(modifier, text='Email:')
        email_saisie = ttk.Entry(modifier)
        email_saisie.insert(0,f"{cnid[0]['Email']}")

        curent = tv.focus()
        value = tv.item(curent)['values']

        # =============== Objets pour Verifier les inputes ===============
        verifier_nom = Verifier("Nom", modifier, r"^[A-Z]{1}[a-z]+$","Omari")
        verifier_prenom = Verifier("Prenom", modifier, r"^[A-Z]{1}[a-z]+$","Karim")
        verifier_age = Verifier("Age", modifier, r"^\d{1,3}$","25")
        verifier_email = Verifier("Email", modifier, r"^[\w\._\-]+@\w+\.[a-z]{3,4}$","exemple@gmail.com")
        def modif():
            for i in range(len(data)-1,-1,-1):
                if(data[i]['Cni'] == cnid[0]['Cni']):
                    if (verifier_nom.verifier_format(nom_saisie.get()) and verifier_prenom.verifier_format(pre_saisie.get()) and verifier_age.verifier_format(age_saisie.get()) and verifier_email.verifier_format(email_saisie.get())):
                        data[i]['Nom'] = nom_saisie.get()
                        data[i]['Prenom'] = pre_saisie.get()
                        data[i]['Age'] = age_saisie.get()
                        data[i]['Email'] = email_saisie.get()
                        value[0] = cne_saisie.get()
                        data_tuples = (cne_saisie.get(), nom_saisie.get() ,pre_saisie.get() , age_saisie.get(), email_saisie.get())
                        tv.delete(curent)
                        tv.insert('', i, values=data_tuples)
                        modifier.destroy()

        btn_modif = ttk.Button(modifier,text="Modifier", command=modif)

        m.pack()

        cne.place(x=50, y=40)
        cne_saisie.place(x=100, y=40)

        nom.place(x=50,y=70)
        nom_saisie.place(x=100,y=70)

        prenom.place(x=50, y=100)
        pre_saisie.place(x=100, y=100)

        age.place(x=50, y=130)
        age_saisie.place(x=100, y=130)

        email.place(x=50, y=160)
        email_saisie.place(x=100, y=160)

        btn_modif.place(x = 120, y=210)

# =============== Suprimer Stagiare ===============
def suprimer_stagiare(evt):
    curItem = tv.focus()
    value = tv.item(curItem)['values']
    note_view.delete(*note_view.get_children())
    if(len(value)>0):
        for i in range(len(data)-1, -1, -1):
            if data[i]['Cni'] == value[0]:
                del data[i]
                tv.delete(curItem)
                note_view.selection_clear()

# =============== Ajouter Module ===============
def ajouter_module(evt):
    modules = []
    if(len(cnid)>0):
        ajouter = tk.Tk()
        ajouter.geometry('300x280')

        m = ttk.Label(ajouter, text="Ajouter Stagiaire")

        module = ttk.Label(ajouter, text='Module:')
        module_saisie = ttk.Entry(ajouter)

        note = ttk.Label(ajouter, text='Note:')
        note_saisie = ttk.Entry(ajouter)

        btn_ajout = ttk.Button(ajouter,text="Ajouter")

        m.pack()

        module.place(x=50, y=40)
        module_saisie.place(x=100, y=40)

        note.place(x=50,y=70)
        note_saisie.place(x=100,y=70)

        btn_ajout.place(x = 120, y=210)

        verifier_module = Verifier("Module", ajouter,r"^[A-Z]{1}[a-z]+$", "Python")
        verifier_note = Verifier("Note", ajouter,r"^((0|[2-9]|[1][\d]{0,1}?|19)(\.\d{1,2})?|20(\.0)?)$","19.5")


        def ajout_note(evt):
            if (verifier_module.verifier_format(module_saisie.get()) and verifier_note.verifier_format(note_saisie.get())):

                mod = module_saisie.get()
                nte = note_saisie.get()

                note_module2 = (mod , nte)

                modules.append(note_module2)
                notes_dict = {}

                for subject, grade in modules:
                    notes_dict[subject] = grade

                for row in data:
                    if row['Cni'] == cnid[0]['Cni']:
                        if module_saisie.get() not in row['Note']:
                            row['Note'].update(notes_dict)
                            note_view.insert('', 'end', values=note_module2)

                        else:
                            tkinter.messagebox.showwarning("Attention", "Cette matiere déja existe, tu peut le modifier", parent=ajouter)
        btn_ajout.bind("<Button-1>", ajout_note)

# =============== Modufier Module ===============
def modifier_module(evt):
    if(len(cnid)>0):
        curent = note_view.focus()
        value = note_view.item(curent)['values']
        if len(value)>0:
            modifier_note = tk.Tk()
            modifier_note.geometry('300x280')
            m = ttk.Label(modifier_note, text="Modifier Stagiaire")

            module = ttk.Label(modifier_note, text='Module:')
            module_saisie = ttk.Entry(modifier_note)
            module_saisie.insert(0,f"{value[0]}")
            module_saisie.configure(state='disabled')

            note = ttk.Label(modifier_note, text='Note:')
            note_saisie = ttk.Entry(modifier_note)
            note_saisie.insert(0,f"{value[1]}")

            verifier_note = Verifier("Note", modifier_note, r"^((0|[2-9]|[1][\d]{0,1}?|19)(\.\d{1,2})?|20(\.0)?)$", "19.5")

            def modif_note():
                index = 0
                if (verifier_note.verifier_format(note_saisie.get())):
                    for i in range(len(data)-1,-1,-1):
                        if(data[i]['Cni'] == cnid[0]['Cni']):
                            data[i]['Note'][f'{value[0]}'] = note_saisie.get()
                            data_tuples = (module_saisie.get(), note_saisie.get())
                            note_view.delete(curent)
                            for j in cnid[0]['Note']:
                                if j in value:
                                    note_view.insert('', index, values=data_tuples)
                                index += 1
                            modifier_note.destroy()

            btn_modif = ttk.Button(modifier_note,text="Modifier", command=modif_note)

            m.pack()

            module.place(x=50, y=40)
            module_saisie.place(x=100, y=40)

            note.place(x=50,y=70)
            note_saisie.place(x=100,y=70)

            btn_modif.place(x = 120, y=210)

# =============== Suprimer Module ===============
def suprimer_module(evt):
    curItem_tv = tv.focus()
    value_tv = tv.item(curItem_tv)['values']
    curItem = note_view.focus()
    value = note_view.item(curItem)['values']
    if len(value) > 0:
        for i in range(len(data) - 1, -1, -1):
            if data[i]['Cni'] == value_tv[0]:
                del data[i]['Note'][value[0]]
                note_view.delete(curItem)

# =============== Enregistrer ===============
def enregistrer(evt):
    with open("Stagiare.json", "w") as f:
        f.write(json.dumps(data, indent=2))
        tkinter.messagebox.showinfo("Notification", "Enregistrer avec succe", parent=app)


# =============== Clicke Des Bouttons ===============
enre.bind("<Button-1>", enregistrer)
ajout.bind("<Button-1>", ajouter_stagiare)
mod.bind("<Button-1>", modifier_stagiare)
sup.bind("<Button-1>", suprimer_stagiare)
a_module.bind("<Button-1>", ajouter_module)
m_module.bind("<Button-1>", modifier_module)
s_module.bind("<Button-1>", suprimer_module)

tv.bind('<<TreeviewSelect>>', click_row)

app.mainloop()
