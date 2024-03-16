from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login Details")
        self.root.geometry("800x700+0+0")

        #====Login frame
        self.employee_id=StringVar()
        self.password=StringVar()
        
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=200,y=60,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("goudy old style",20,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("goudy old style",15),bg="white").place(x=50,y=100)
        txt_employee_id=Entry(login_frame,textvariable=self.employee_id,font=("goudy old style",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("goudy old style",15),bg="white").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("goudy old style",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,text="Login",command=self.login,font=("goudy old style",15),bg="#00B0F0",activebackground="#00B0F0",cursor="hand2").place(x=50,y=300,width=250,height=35)
        
        #hr=Label(login_frame,bg="lightgrey").place(x=50,y=360,width=250,height=2)

        btn_forget=Button(login_frame,text="Forget Password?",font=("times new roman",13),bg="white",fg="#00759E",bd=0).place(x=100,y=360)

    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror('Error',"All fields are required",parent=self.root)
            else:
                cur.execute("Select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror('Error',"Invalid username or password",parent=self.root)
                else:
                    #print(user)
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)  

    
    

        
root=Tk()
obj=Login_System(root)
root.mainloop()