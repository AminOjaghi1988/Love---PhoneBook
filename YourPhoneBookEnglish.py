from sqlite3.dbapi2 import enable_callback_tracebacks
from sys import dllhandle
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from typing import Sized, no_type_check
from PIL import ImageTk, Image
from functools import partial 


win = Tk()

win.geometry("1250x800")

win.resizable(False, False)

win.title('PhoneBook Of Manoochehr')

win.iconbitmap('icon.ico')



conn = sqlite3.connect('DBphonebook.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS phonebook(
           Name text,
           Familly text,
           Number integer,
           Address text
           )""")

conn.commit()

conn.close()


my_pic = Image.open('pic4.jpg')

resized = my_pic.resize((1250,800),Image.ANTIALIAS)

new_pic = ImageTk.PhotoImage(resized)

my_label = Label(win, image=new_pic)
my_label.pack()

God_Label = Label(win, text='@ Power Of Inteligence Is Power Of God', background='White')
God_Label.place(x=0, y=0)

lb = Label(win, text=': Name', font=5)
lb.place(x=900, y=40)

en = Entry(win , width = 60, bd = 3, font=('Arial', 15) )
en.place(x = 225, y = 42)

lb1 = Label(win, text=': Familly', font=5)
lb1.place(x=835, y=90)

en1 = Entry(win , width = 60 , bd = 3, font=('Arial', 15) )
en1.place(x=160 , y=93)

lb2 = Label(win, text=': Number', font=5)
lb2.place(x=840, y=195)

en2 = Entry(win , width = 60 , bd = 3, font=('Arial', 15) )
en2.place(x = 160 , y = 195)

lb3 = Label(win, text=': Address', font=5)
lb3.place(x=885, y=245)

en3 = Entry(win , width = 65, bd = 3, font=('Arial', 15))
en3.place(x = 150 , y = 246)


def savebtn():
    conn = sqlite3.connect('DBphonebook.db')

    c = conn.cursor()

    c.execute("INSERT INTO phonebook(Name, Familly, Number, Address) VALUES('%s', '%s', '%s', '%s')"
    %(en.get(), en1.get(), en2.get(), en3.get()))

    conn.commit()

    conn.close()

    messagebox.showinfo("Success" , "Done!")

    en.delete(0, END)
    en1.delete(0, END)
    en2.delete(0, END)
    en3.delete(0, END)

btn = Button(win, text='Save', padx=50, pady=10, font=20, background='pink', command=savebtn)
btn.place(x= 700, y=350)



def clear_edit_btn():

    global records, l

    conn = sqlite3.connect('DBphonebook.db')

    c = conn.cursor()

    c.execute('SELECT * FROM phonebook')

    records = c.fetchall()

    x = 0

    top1 = Toplevel()

    top1.geometry("1400x700")
    top1.resizable(False, False)
    top1.iconbitmap('icon.ico')
    top1.title('Edit & Delete')

    main_frame = Frame(top1)
    main_frame.pack(fill=BOTH, expand=1, pady=66)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    def _on_mouse_wheel(event):
        my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
    my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

    second_frame = Frame(my_canvas)
    second_frame.configure(background='Green')

    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    
    def deletefunc():

        top2 = Toplevel(background='Blue')

        top2.geometry("500x300")
        top2.iconbitmap('icon.ico')
        top2.title('Delete')

        lb = Label(top2, text=': Inser Name Who Want To Delete', font=5, background='Pink')
        lb.place(x=175, y=10)

        en = Entry(top2, width = 43, bd = 3, font=('Arial', 15))
        en.place(x=10, y=50)

        lb1 = Label(top2, text=': Insert Familly Who Want To Delete', font=5, background='Pink')
        lb1.place(x=125, y=120)

        en1 = Entry(top2, width = 43, bd = 3, font=('Arial', 15))
        en1.place(x=10, y=160)

        def deletebtn():

            conn = sqlite3.connect('DBphonebook.db')

            c = conn.cursor()

            c.execute('SELECT * FROM phonebook')

            list_of_records = c.fetchall()

            for record_of_loop in list_of_records:
            
                if record_of_loop[0] == en.get() and record_of_loop[1] == en1.get():

                    conn = sqlite3.connect('DBphonebook.db')

                    c = conn.cursor()

                    c.execute("DELETE from phonebook WHERE Name= :Name AND Familly= :Familly", {'Name':en.get(), 'Familly':en1.get()})

                    conn.commit()

                    conn.close()

                    top2.destroy()

                    top1.destroy()

                    clear_edit_btn()
                
                            
                else:

                    messagebox.showerror("Error", "Name And Familly Does,nt Exists !") 
                    top2.destroy()  
            

        deletebutton = Button(top2, text='D  E  L  E  T  E', command=deletebtn, width=30, height=1, bd=3, background='Pink', font='Bold')
        deletebutton.place(x=20, y=230)


        


    def editfunc():
        
        top3 = Toplevel(background='Blue')

        top3.geometry("750x350")
        top3.iconbitmap('icon.ico')
        top3.title('Edit')

        lb50 = Label(top3, text=': Insert Name Who Want To Edit', font=5, background='Pink')
        lb50.place(x=410, y=10)

        en50 = Entry(top3, width = 65, bd = 3, font=('Arial', 15))
        en50.place(x=15, y=50)

        lb51 = Label(top3, text=': Insert Familly Who Want To Edit', font=5, background='Pink')
        lb51.place(x=355, y=120)

        en51 = Entry(top3, width = 65, bd = 3, font=('Arial', 15))
        en51.place(x=15, y=160)

        def editfunc1():

            conn = sqlite3.connect('DBphonebook.db')

            c = conn.cursor()

            c.execute('SELECT * FROM phonebook')

            list_of_records1 = c.fetchall()

            for record_of_loop1 in list_of_records1:
            
                if record_of_loop1[0] == en50.get() and record_of_loop1[1] == en51.get():

                    conn = sqlite3.connect('DBphonebook.db')

                    c = conn.cursor()

                    c.execute("SELECT * FROM phonebook WHERE Name= :Name AND Familly= :Familly", {'Name':en50.get(), 'Familly':en51.get()})

                    records = c.fetchall()

                    top4 = Toplevel(background='Blue')
                    top4.geometry("750x500")
                    top4.iconbitmap('icon.ico')
                    top4.title('Edit')

                    lb100 = Label(top4, text=': Apply Your Change', font=0, background='Pink')
                    lb100.place(x=480, y=50)

                    en100 = Entry(top4, width = 65, bd = 3, font=('Arial', 15))
                    en100.place(x=15, y=100)

                    en200 = Entry(top4, width = 65, bd = 3, font=('Arial', 15))
                    en200.place(x=15, y=150)

                    en300 = Entry(top4, width = 65, bd = 3, font=('Arial', 15))
                    en300.place(x=15, y=200)

                    en400 = Entry(top4, width = 65, bd = 3, font=('Arial', 15))
                    en400.place(x=15, y=250)

                    label = Label(top4, text='If You Want Change Just Name Do It Single And Other Together : Attention', font=0, background='Pink')
                    label.place(x=70, y=450)

                    for record in records:
                        en100.insert(0, record[0])
                        en200.insert(0, record[1])
                        en300.insert(0, record[2])
                        en400.insert(0, record[3])

                else:

                    messagebox.showerror("Error", "Name And Familly Does,nt Exists !")
                    top3.destroy()      
            
            def editfunc2():
                conn = sqlite3.connect('DBphonebook.db')

                c = conn.cursor()

                c.execute("""UPDATE phonebook SET
                        Name = :Name,
                        Familly = :Familly,
                        Number = :Number,
                        Address = :Address

                        WHERE Name= :Name""", 
                        {
                            'Name':en100.get(), 
                            'Familly':en200.get(),
                            'Number':en300.get(),
                            'Address':en400.get()
                        })
                c.execute("""UPDATE phonebook SET
                        Name = :Name,
                        Familly = :Familly,
                        Number = :Number,
                        Address = :Address

                        WHERE Address= :Address""", 
                        {
                            'Name':en100.get(), 
                            'Familly':en200.get(),
                            'Number':en300.get(),
                            'Address':en400.get()
                        })


                conn.commit()
                conn.close()

                top4.destroy()
                top1.destroy()
                clear_edit_btn()



            
            editbutton1 = Button(top4, text='U  p  d  a  t  e  ...', command=editfunc2, width=59, height=2, bd=3, background='Pink', font='Bold')

            editbutton1.place(x=50, y=350)

            conn.commit()

            conn.close()

            top3.destroy()

        editbutton = Button(top3, text='Click For Edit', command=editfunc1, width=59, height=2, bd=3, background='Pink', font='Bold')

        editbutton.place(x=50, y=220)
    

    deletebutton = Button(top1, text='D   E   L   E   T', command=deletefunc, width=61, height=2, bd=3, background='Pink', font='Bold')

    deletebutton.place(x=2, y=3)

    editbutton = Button(top1, text='E   D   I   T', command=editfunc, width=61, height=2, bd=3, background='Pink', font='Bold')

    editbutton.place(x=698, y=3)



    lbl100 = Label(second_frame, text='Address', font=('Bold', 18), background='Blue')
    lbl100.grid(row=1, column=150, padx=300, pady=10)

    lbl200 = Label(second_frame, text='Number', font=('Bold', 18), background='Blue')
    lbl200.grid(row=1, column=200, padx=70, pady=10)

    lbl300 = Label(second_frame, text='Familly', font=('Bold', 18), background='Blue')
    lbl300.grid(row=1, column=250, padx=70, pady=10)

    lbl400 = Label(second_frame, text='Name', font=('Bold', 18), background='Blue')
    lbl400.grid(row=1, column=300, padx=70, pady=10)


    records.sort()

    for record in records:

        x += 20        

        Label(second_frame, text=record[3], font=('Bold', 10), background='Pink').grid(row=x, column=150, pady=10, padx=300)

        Label(second_frame, text=record[2], font=('Bold', 10), background='Pink').grid(row=x, column=200, pady=10, padx=70)

        Label(second_frame, text=record[0], font=('Bold', 10), background='Pink').grid(row=x, column=300, pady=10, padx=70)

        Label(second_frame, text=record[1], font=('Bold', 10), background='Pink').grid(row=x, column=250, pady=10, padx=70)

btn1 = Button(win, text='List , Edit & Delete', padx=50, pady=10, font=20, background='pink', command=clear_edit_btn)
btn1.place(x= 300, y=350)




lb4 = Label(win, text=': Search In Phonebook', font=5, background='Red')
lb4.place(x=800, y=460)

lb5 = Label(win, text=': Insert Name', font=5)
lb5.place(x=810, y=510)

en4 = Entry(win , width = 55, bd = 4, font=('Arial', 15))
en4.place(x = 180 , y = 510)

lb6 = Label(win, text=': Insert Familly', font=5)
lb6.place(x=750, y=570)

en5 = Entry(win , width = 50, bd = 4, font=('Arial', 15))
en5.place(x = 180 , y = 565)

def searchbtn():

    a = 0

    connection = sqlite3.connect('DBphonebook.db')

    c = connection.cursor()

    c.execute("SELECT * FROM phonebook WHERE Name= :Name AND Familly= :Familly", {'Name':en4.get(), 'Familly':en5.get()})

    records1 = c.fetchall()

    for record1 in records1:

        lb01 = Label(win, text=record1[0], font=('Bold', 15), background='Pink')
        lb01.place(x= 800, y=700)

        lb02 = Label(win, text=record1[1], font=('Bold', 15), background='Pink')
        lb02.place(x= 650, y=700)

        lb03 = Label(win, text=record1[2], font=('Bold', 15), background='Pink')
        lb03.place(x= 450, y=700)

        lb04 = Label(win, text=record1[3], font=('Bold', 15), background='Pink')
        lb04.place(x=250, y=700)

btn2 = Button(win, text='S  e  a  r  c  h', padx=200, pady=1, font=20, background='pink', command=searchbtn)
btn2.place(x= 300, y=620)

win.mainloop()