from tkinter import*
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass 
import sqlite3
from tkinter import messagebox
import os
import time

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        
        title=Label(self.root,text="Inventory Management System",font=("times new roman",40,"bold"),bg="#0000EE",fg="#FFEBCD",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
        btn_logout=Button(self.root,command=self.logout,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
        self.lbl_clock=Label(self.root,text="Welcome To Inventory Management System\t\t Date:DD-MM-YYYY\t\t Time: HH-MM-SS",font=("times new roman",15,),bg="#E0EEEE",fg="#000000")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        self.MenuLogo=Image.open("S:\IMS repo/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.LANCZOS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)
        
        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)
        
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#458B00").pack(side=TOP,fill=X)
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_products=Button(LeftMenu,text="Products",command=self.product,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
       #btn_sales=Button(LeftMenu,text="Sales",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",command=self.exit,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        self.lbl_employee=Label(self.root,text="Total Employees\n[0]",bg="#6495ED",fg="white",font=("times new roman",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)
        
        self.lbl_supplier=Label(self.root,text="Total Suppliers\n[0]",bg="#00EEEE",fg="white",font=("times new roman",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)
        
        self.lbl_category=Label(self.root,text="Total Categories\n[0]",bg="#FFB90F",fg="white",font=("times new roman",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)
        
        self.lbl_product=Label(self.root,text="Total Products\n[0]",bg="#FF7F00",fg="white",font=("times new roman",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)
        
        self.lbl_sales=Label(self.root,text="Total Sales\n[0]",bg="#BF3EFF",fg="white",font=("times new roman",20,"bold"))
        self.lbl_sales.place(x=650 ,y=300,height=150,width=300)


        self.update_content()
        
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self): 
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()

        try:
            cur.execute("Select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f"Total Products\n[{str(len(product))}]")

            cur.execute("Select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n[{str(len(supplier))}]")

            cur.execute("Select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[{str(len(category))}]")

            cur.execute("Select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f"Total employee\n[{str(len(employee))}]")

            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f"Total Sales\n[{str(len(os.listdir('bill')))}]")

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome To Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)



        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)    

    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    def exit(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()