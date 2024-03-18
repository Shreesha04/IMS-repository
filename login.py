from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib #pip install smtplib
import time

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login Details")
        self.root.geometry("800x700+0+0")

        self.otp=''

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

        btn_forget=Button(login_frame,command=self.forget_window,text="Forget Password?",font=("times new roman",13),bg="white",fg="#00759E",bd=0).place(x=110,y=360)

        #new user contact admin
        lbl_new_user=Label(login_frame,text="New User?\nContact Admin",font=("goudy old style",13),bg="white",justify=CENTER).place(x=115,y=390)
       

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

    def forget_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            if self.employee_id.get()=="":
                messagebox.showerror('Error',"Employee ID must be required",parent=self.root)
            else: 
                cur.execute("Select email from employee where eid=? ",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror('Error',"Invalid Empoyee ID",parent=self.root)
                else:
                    #forget window
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_con_pass=StringVar()
                    #call send_email func
                    chk=self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror('Error',"Connection error,try again",parent=self.root)
                    else:
                    

                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title('Reset Password')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text='Reset Password',font=("goudy old style",15,"bold")).pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter Otp sent on registered email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                        
                        self.btn_reset=Button(self.forget_win,text="Submit",command=self.validate_otp,font=("times new roman",15),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)
                        
                        lbl_c_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=225)
                        txt_c_pass=Entry(self.forget_win,textvariable=self.var_con_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)
                        

                        self.btn_update=Button(self.forget_win,command=self.update_password,text="Update",state=DISABLED,font=("times new roman",15),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)  

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_con_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get()!= self.var_con_pass.get():
            messagebox.showerror("Error","Password should be same",parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()

            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password updated successfully",parent=self.forget_win)
                self.forget_win.destroy()

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)  


    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        
        subj='IMS-Research Password OTP'
        msg=f'Desr Sir/Madam,\n\nYour reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team'

        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'
        
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror('Error',"Invalid OTP,try again",parent=self.forget_win)

        
root=Tk()
obj=Login_System(root)
root.mainloop()