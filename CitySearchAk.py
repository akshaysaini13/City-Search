# Importing libraries

from tkinter import *
from PIL import Image,ImageTk
from tkinter.ttk import Combobox
from tkinter import messagebox
import sqlite3
from tkinter.scrolledtext import ScrolledText

# Creating tables in DB
try:
    con=sqlite3.connect(database="database/city.sqlite")
    cursor=con.cursor()
    cursor.execute("create table post(cat_name text,name text,adr text,post_by text,isApprove text)")
    cursor.execute("create table users(username text primary key,password text)")
    cursor.execute("create table category(cat_name text primary key)")
    con.commit()
    print("table created")
except:
    print("table already exists")
con.close()


win=Tk() # Instantiating Tkinter class object 

# setting up windows size
win.state("zoomed")
win.title("CITY SEARCH")

# Setting up background image and converting to Tkinter format
imgbg=Image.open("images/img4.jpg").resize((2100,1024))
imgbgtk=ImageTk.PhotoImage(imgbg,master=win)
lbg=Label(win,image=imgbgtk,bg="black")
lbg.place(x=0,y=0)
win.resizable(width=False,height=False)

# Opening image files and converting to Tkinter format
img_logo1= Image.open("images/img1.1.jfif").resize((150,100))
imgtk_logo1=ImageTk.PhotoImage(img_logo1,master=win)
lbl_logo1=Label(win,image=imgtk_logo1)
lbl_logo1.place(relx=.65,y=35)

img_logo2= Image.open("images/img14.1.png").resize((450,100))
imgtk_logo2=ImageTk.PhotoImage(img_logo2,master=win)
lbl_logo2=Label(win,image=imgtk_logo2)
lbl_logo2.place(relx=.37,y=35)

img_logo3= Image.open("images/img1.1.jfif").resize((150,100))
imgtk_logo3=ImageTk.PhotoImage(img_logo3,master=win)
lbl_logo3=Label(win,image=imgtk_logo3)
lbl_logo3.place(relx=.275,y=35)

img_frame=Image.open("images/img15.jpg").resize((1000,500))
imgtk_frame=ImageTk.PhotoImage(img_frame,master=win)

img_frame2=Image.open("images/img21.jpg").resize((1000,500))
imgtk_frame2=ImageTk.PhotoImage(img_frame2,master=win)

img_frame3=Image.open("images/img19.jpg").resize((1000,500))
imgtk_frame3=ImageTk.PhotoImage(img_frame3,master=win)

img_login=Image.open("images/login.png").resize((110,40))
imgtk_login=ImageTk.PhotoImage(img_login,master=win)

img_reset=Image.open("images/reset.png").resize((110,40))
imgtk_reset=ImageTk.PhotoImage(img_reset,master=win)

img_newuser=Image.open("images/newuser.png").resize((180,40))
imgtk_newuser=ImageTk.PhotoImage(img_newuser,master=win)

img_search=Image.open("images/Search1.png").resize((110,40))
imgtk_search=ImageTk.PhotoImage(img_search,master=win)

img_logout=Image.open("images/logout.png").resize((110,40))
imgtk_logout=ImageTk.PhotoImage(img_logout,master=win)

img_back=Image.open("images/c.jpg").resize((90,40))
imgtk_back=ImageTk.PhotoImage(img_back,master=win)

img_backn=Image.open("images/bn 2.png").resize((90,40))
imgtk_backn=ImageTk.PhotoImage(img_backn,master=win)

img_add=Image.open("images/add2.png").resize((110,40))
imgtk_add=ImageTk.PhotoImage(img_add,master=win)

img_nframe=Image.open("images/d.jpg").resize((1000,500))
imgtk_nframe=ImageTk.PhotoImage(img_nframe,master=win)

img_dlt=Image.open("images/dlt.jfif").resize((110,40))
imgtk_dlt=ImageTk.PhotoImage(img_dlt,master=win)

lbl_search=Label(win,text="Select Category",font=("Arial",15,'bold'),bg='#0b0716',fg='white')
lbl_search.place(relx=.62,rely=.3)


def show_cat():
    """
    Function to connect with database and shows all the listed categories in the table
    """
    con=sqlite3.connect(database="database/city.sqlite")
    cursor=con.cursor()
    cursor.execute("select cat_name from category")
    global cb_search
    cb_search=Combobox(win,font=('Arial',16,'bold'),values=cursor.fetchall())
    cb_search.current(0)
    cb_search.place(relx=.77,rely=.30)
    con.close()

show_cat()

st=ScrolledText(win,height=18,width=60)
st.place(relx=.6,rely=.4)
st.insert("end","Category\t\tName\t\tAddress\n")
st.insert("end","-----------------------------------------------\n")


def search_post(event): 
    """
    List catogory and name, selected by user which are approved by Admin
    """
    cat=cb_search.get()
    con=sqlite3.connect(database="database/city.sqlite")
    cursor=con.cursor()
    cursor.execute("select * from post where isApprove='yes' and cat_name=?",(cat,))
    info=""
    for row in cursor:
        info=info+"\n"+row[0]+"\t\t"+row[1]+"\t\t"+row[2]+"\t\t\t"
        
    st.insert("end",info)
    

search_btn=Label(win,image=imgtk_search,bg='#0b0a15')
search_btn.place(relx=.87,rely=.35)
search_btn.bind("<Button>",search_post)   


def main_frame():
    """
    Main frame function comprising of all the elements to enter username, password, 
    Type of user with Login, Signup and Reset button
    """
    frm=Frame(win,bg="black")
    frm.place(relx=.05,rely=.30,relwidth=.5,relheight=.6)
    
    def reset(event):
        """
        Eventlistner for reset button
        """
        e_user.delete(0,"end")
        e_pass.delete(0,'end')
        e_user.focus()
        
    def login(event):
        """
        Eventlistner for Login button
        """
        u=e_user.get()
        p=e_pass.get()
        if(len(u)==0 or len(p)==0):
            messagebox.showerror("Validation","Username/Password can't be empty")
        else:
            utype=cb_type.get()
            if(utype=='Admin'):
                if(u.lower()=="admin"and p.lower()=='admin'):
                    frm.destroy()
                    welcome_admin_frame()
                else:
                    frm.destroy()
                    messagebox.showerror("Login","Invalid user Username/Password ")
            else:
                con=sqlite3.connect(database="database/city.sqlite")
                cursor=con.cursor()
                cursor.execute("select * from users where username=? and password=?",(u,p))
                global row_user
                row_user=cursor.fetchone()
                if(row_user==None):
                    messagebox.showerror("Login","Invalid user Username/Password ")
                else:
                    frm.destroy()
                    welcome_user_frame()
            
    def newuser(event):
        """
        Eventlistner for Signup button
        """
        frm.destroy()
        new_user_frame()
        

        
    frame_btn=Label(frm,image=imgtk_frame,bg="black")
    frame_btn.place(relx=.0,rely=.0)
    
    lbl_user=Label(frm,font=('Arial',18,'bold'),text="Username",fg='white',bg='#000a23')
    lbl_user.place(relx=.14,rely=.1)
    
    lbl_pass=Label(frm,font=('Arial',18,'bold'),text="Password",fg='white',bg='#000a23')
    lbl_pass.place(relx=.14,rely=.25)
    
    lbl_Type=Label(frm,font=('Arial',18,'bold'),text="Type",fg='white',bg='#000a23')
    lbl_Type.place(relx=.14,rely=.4)
    
    e_user=Entry(frm,font=('Arial',18,'bold'),bd=5,fg="black")
    e_user.place(relx=.4,rely=.1)
    e_user.focus()
    
    e_pass=Entry(frm,font=('Arial',18,'bold'),bd=5,fg="black",show='*')
    e_pass.place(relx=.4,rely=.25)
    
    cb_type=Combobox(frm,font=('Arial',15,'bold'),values=['User','Admin'])
    cb_type.place(relx=.4,rely=.4)
    cb_type.current(0)
    
    login_btn=Label(frm,image=imgtk_login,bg='#031c44')
    login_btn.place(relx=.3,rely=.56)
    login_btn.bind("<Button>",login)
    
    reset_btn=Label(frm,image=imgtk_reset,bg='#031c44')
    reset_btn.place(relx=.5,rely=.56)
    reset_btn.bind("<Button>",reset)
    
    newuser_btn=Label(frm,image=imgtk_newuser,bg='#003366')
    newuser_btn.place(relx=.38,rely=.75)
    newuser_btn.bind("<Button>",newuser)
    

def new_user_frame():
    """
    Sign up frame for new user
    """

    def back(event):
        """
        Eventlistner for Back button
        """
        frm.destroy()
        main_frame()
    
    def create_account():
        """
        Command function for new user account creation
        """
        u=e_user.get()
        p=e_pass.get()
        if(len(u)==0 or len(p)==0):
            messagebox.showerror("Validation","Username/Password can't be empty")
        else:
            try:
                con=sqlite3.connect(database="database/city.sqlite")
                cursor=con.cursor()
                cursor.execute("insert into users values(?,?)",(u,p))
                con.commit()
                messagebox.showinfo("Account","Account created")
                frm.destroy()
                main_frame()
            except:
                messagebox.showerror("Account","Username already exists")
            con.close()
            
    frm=Frame(win)
    frm.place(relx=.1,rely=.30,relwidth=.5,relheight=.6)
    
    frame_btn=Label(frm,image=imgtk_nframe,bg="black")
    frame_btn.place(relx=.0,rely=.0)
    
    lbl_user=Label(frm,font=('Arial',18,'bold'),text="Username",fg='white',bg='#012c4c')
    lbl_user.place(relx=.15,rely=.2)
    
    lbl_pass=Label(frm,font=('Arial',18,'bold'),text="Password",fg='white',bg='#032842')
    lbl_pass.place(relx=.14,rely=.38)
    
    e_user=Entry(frm,font=('Arial',18,'bold'),bd=5,fg="black")
    e_user.place(relx=.4,rely=.2)
    e_user.focus()
    
    e_pass=Entry(frm,font=('Arial',18,'bold'),bd=5,fg="black",show='*')
    e_pass.place(relx=.4,rely=.38)
    
    create_act_btn=Button(frm,text="Create Account",width=15,font=("Arial",16,'bold'),bd=5,command=create_account)
    create_act_btn.place(relx=.36,rely=.57)
    
    lbl_back=Label(frm,image=imgtk_backn,bg="#9ca9b1")
    lbl_back.place(x=670,y=445)
    lbl_back.bind("<Button>",back)

    

def welcome_admin_frame():
    """
    Admin frame after Logging in as Admin
    """
    
    frm=Frame(win,bg="black")
    frm.place(relx=.05,rely=.30,relwidth=.5,relheight=.6)
    
    frame_btn=Label(frm,image=imgtk_frame3,bg="black")
    frame_btn.place(relx=.0,rely=.0)
    
    def logout(event):
        """
        Eventlistner for Logout button
        """
        frm.destroy()
        main_frame()
        
    def add():
        """
        Command function for adding new category for Admin
        """
        frm.destroy()
        add_cat_frame()
        
    def info():
        """
        Command function for Posting information
        """
        frm.destroy()
        post_info_frame()
        
    def apr():
        """
        Command fucntion for Approving post requested by users
        """
        frm.destroy()
        post_apr_frame()
    
    def dlt():
        """
        Command function for deleting category
        """
        frm.destroy()
        dlt_cat_frame()


    lbl_wel=Label(frm,text="Welcome,Admin",font=('Arial',12),bg="#51b7bb",fg='white')
    lbl_wel.place(x=5,y=5)
    
    lbl_logout=Label(frm,image=imgtk_logout,bg="#76d4bc")
    lbl_logout.place(relx=.8,rely=.02)
    lbl_logout.bind("<Button>",logout)
    
    add_cat_btn=Button(frm,command=add,text="Add Category",width=15,font=("Arial",16,'bold'),bd=5)
    add_cat_btn.place(relx=.38,rely=.10)
    
    post_info_btn=Button(frm,command=info,text="Post Information",width=15,font=("Arial",16,'bold'),bd=5)
    post_info_btn.place(relx=.38,rely=.30)
    
    post_ap_btn=Button(frm,command=apr,text="Approve Post",width=15,font=("Arial",16,'bold'),bd=5)
    post_ap_btn.place(relx=.38,rely=.50)
    
    dlt_ap_btn=Button(frm,command=dlt,text="Delete Category",width=15,font=("Arial",16,'bold'),bd=5)
    dlt_ap_btn.place(relx=.38,rely=.70)


def welcome_user_frame():
    """
    User frame after logging in as a generic user
    """
    
    frm=Frame(win,bg="black")
    frm.place(relx=.05,rely=.30,relwidth=.5,relheight=.6)
    
    frame_btn=Label(frm,image=imgtk_frame3,bg="black")
    frame_btn.place(relx=.0,rely=.0)
    
    def logout(event):
        """
        Command function for Logout button
        """
        frm.destroy()
        main_frame()
        
    def add():
        """
        Command function for adding category
        """
        frm.destroy()
        add_cat_frame()
        
    def info_by_user():
        """
        Command function for posting information
        """
        frm.destroy()
        post_info_userframe()
        

    lbl_wel=Label(frm,text=f"Welcome,{row_user[0]}",font=('Arial',12),bg="#51b7bb",fg='white')
    lbl_wel.place(x=5,y=5)
    
    lbl_logout=Label(frm,image=imgtk_logout,bg="#76d4bc")
    lbl_logout.place(relx=.8,rely=.02)
    lbl_logout.bind("<Button>",logout)
    
    post_info_btn=Button(frm,command=info_by_user,text="Post Information",width=15,font=("Arial",16,'bold'),bd=5)
    post_info_btn.place(relx=.38,rely=.30)
       
    
def add_cat_frame():
    """
    Frame for adding new category by Admin
    """
    
    frm=Frame(win,bg="black")
    frm.place(relx=.05,rely=.30,relwidth=.5,relheight=.6)
    
    frame_btn=Label(frm,image=imgtk_frame3,bg="black")
    frame_btn.place(relx=.0,rely=.0)
    
    def logout(event):
        """
        Eventlistner for Logout button
        """
        frm.destroy()
        main_frame()
        
    def back(event):
        """
        Eventlistner for back button
        """
        frm.destroy()
        welcome_admin_frame()
        
    def add_db(event):
        """
        Eventlistner to add category in database
        """
        cat=e_cat.get()
        if(len(cat)==0):
            messagebox.showerror("Validation","Please enter category")
        else:
            try:
                con=sqlite3.connect(database="database/city.sqlite")
                cursor=con.cursor()
                cursor.execute("insert into category values(?)",(cat.upper(),))
                con.commit()
                messagebox.showinfo("Category","category added")
                show_cat()
            except:
                messagebox.showerror("Category","category already added")
            con.close()
            
        
        
    lbl_wel=Label(frm,text="Welcome,Admin",font=('Arial',12),bg="#51b7bb",fg='white')
    lbl_wel.place(x=5,y=5)
    
    lbl_logout=Label(frm,image=imgtk_logout,bg='#76d4bc')
    lbl_logout.place(relx=.8,rely=.02)
    lbl_logout.bind("<Button>",logout)
    
    lbl_back=Label(frm,image=imgtk_back,bg="#51b7bb")
    lbl_back.place(relx=.02,y=25)
    lbl_back.bind("<Button>",back)
    
    lbl_cat=Label(frm,text="Enter Category",font=('Arial',16),bg="#8ad5ba")
    lbl_cat.place(x=150,y=120)
     
    
    lbl_add=Label(frm,image=imgtk_add,bg='#c3dcbe')
    lbl_add.place(x=495,y=165)
    lbl_add.bind("<Button>",add_db)
    
    e_cat=Entry(frm,font=('Arial',16,'bold'),bd=4)
    e_cat.place(x=350,y=120)
    e_cat.focus()
    
    
def post_info_frame():
    """
    function to post information from the category added
    """
    def logout(event):
        """
        Eventlistner for logout button
        """
        frm.destroy()
        main_frame()
        
    def back(event):
        """
        Eventlistner for back button
        """
        frm.destroy()
        welcome_admin_frame()
    
    def post_db():
        """
        Function to insert values into database posted by Admin
        """
        cat=cb_search.get()
        name=e_name.get()
        adr=e_adr.get()
        post_by="admin"
        isApprove="yes"
        con=sqlite3.connect(database="database/city.sqlite")
        cursor=con.cursor()
        cursor.execute("insert into post values(?,?,?,?,?)",(cat,name,adr,post_by,isApprove))
        con.commit()
        con.close()
        messagebox.showinfo("Post","Information posted")
        e_name.delete(0,"end")
        e_adr.delete(0,"end")
        
    frm=Frame(win,bg="black")
    frm.place(relx=.05,rely=.30,relwidth=.5,relheight=.6)
    
    frame_btn=Label(frm,image=imgtk_frame3,bg="black")
    frame_btn.place(relx=.0,rely=.0)
    
    lbl_wel=Label(frm,text="Welcome,Admin",fg='white',font=('Arial',12),bg="#51b7bb")
    lbl_wel.place(x=5,y=5)
    
    lbl_logout=Label(frm,image=imgtk_logout,bg='#76d4bc')
    lbl_logout.place(relx=.8,rely=.02)
    lbl_logout.bind("<Button>",logout)
    
    lbl_back=Label(frm,image=imgtk_back,bg="#51b7bb")
    lbl_back.place(relx=.02,y=25)
    lbl_back.bind("<Button>",back)
    
    lbl_search=Label(frm,text="Select Category",font=("Arial",15,'bold'),bg="#51b7bb",fg='white')
    lbl_search.place(relx=.15,rely=.1)
    
    lbl_name=Label(frm,text="Name:",font=("Arial",15,'bold'),bg="#51b7bb",fg='white')
    lbl_name.place(relx=.15,rely=.25)
    
    lbl_adr=Label(frm,text="Address:",font=("Arial",15,'bold'),bg="#51b7bb",fg='white')
    lbl_adr.place(relx=.15,rely=.4)
    
    e_name=Entry(frm,font=('Arial',18,'bold'),bd=5,fg="black")
    e_name.place(relx=.4,rely=.25)
    e_name.focus()
    
    e_adr=Entry(frm,font=('Arial',18,'bold'),bd=5,fg="black")
    e_adr.place(relx=.4,rely=.4)
    
    btn_post=Button(frm,text="Post",bd=5,width=7,command=post_db)
    btn_post.place(relx=.5,rely=.6)
    
    def show_cat():
        """
        Function to show all the categories
        """
        con=sqlite3.connect(database="database/city.sqlite")
        cursor=con.cursor()
        cursor.execute("select cat_name from category")
        global cb_search
        cb_search=Combobox(frm,font=('Arial',16,'bold'),values=cursor.fetchall())
        cb_search.current(0)
        cb_search.place(relx=.4,rely=.1)
        con.close()
    show_cat()
    
    
def post_info_userframe():
    """
    Function to post information by user
    """
    
    def logout(event):
        """
        Eventlistner for logout button
        """
        frm.destroy()
        main_frame()
        
    def back(event):
        """
        Eventlistner for back button
        """
        frm.destroy()
        welcome_user_frame()
        
    def post_db():
        """
        function to post information and insert into database
        """
        cat=cb_search.get()
        name=e_name.get()
        adr=e_adr.get()
        post_by=row_user[0]
        isApprove="no"
        con=sqlite3.connect(database="database/city.sqlite")
        cursor=con.cursor()
        cursor.execute("insert into post values(?,?,?,?,?)",(cat,name,adr,post_by,isApprove))
        con.commit()
        con.close()
        messagebox.showinfo("Post","Information posted")
        e_name.delete(0,"end")
        e_adr.delete(0,"end")
    
    

    frm=Frame(win,bg="black")
    frm.place(relx=.05,rely=.30,relwidth=.5,relheight=.6)
    
    frame_btn=Label(frm,image=imgtk_frame3,bg="black")
    frame_btn.place(relx=.0,rely=.0)
    
    lbl_wel=Label(frm,text=f"Welcome,{row_user[0]}",fg='white',font=('Arial',12),bg="#51b7bb")
    lbl_wel.place(x=5,y=5)
    
    lbl_logout=Label(frm,image=imgtk_logout,bg='#76d4bc')
    lbl_logout.place(relx=.8,rely=.02)
    lbl_logout.bind("<Button>",logout)
    
    lbl_back=Label(frm,image=imgtk_back,bg="#51b7bb")
    lbl_back.place(relx=.02,y=25)
    lbl_back.bind("<Button>",back)

    lbl_search=Label(frm,text="Select Category",font=("Arial",15,'bold'),bg="#51b7bb",fg='white')
    lbl_search.place(relx=.15,rely=.1)
    
    lbl_name=Label(frm,text="Name:",font=("Arial",15,'bold'),bg="#51b7bb",fg='white')
    lbl_name.place(relx=.15,rely=.25)
    
    lbl_adr=Label(frm,text="Address:",font=("Arial",15,'bold'),bg="#51b7bb",fg='white')
    lbl_adr.place(relx=.15,rely=.4)
    
    e_name=Entry(frm,font=('Arial',18,'bold'),bd=5,fg="black")
    e_name.place(relx=.4,rely=.25)
    e_name.focus()
    
    e_adr=Entry(frm,font=('Arial',18,'bold'),bd=5,fg="black")
    e_adr.place(relx=.4,rely=.4)
    
    btn_post=Button(frm,text="Post",bd=5,width=7,command=post_db)
    btn_post.place(relx=.5,rely=.6)
    

    def show_cat():
        """
        Function to show all categories
        """
        con=sqlite3.connect(database="database/city.sqlite")
        cursor=con.cursor()
        cursor.execute("select cat_name from category")
        global cb_search
        cb_search=Combobox(frm,font=('Arial',16,'bold'),values=cursor.fetchall())
        cb_search.current(0)
        cb_search.place(relx=.4,rely=.1)
        con.close()
    show_cat()


def post_apr_frame():
    """
    Function to approve post posted by general users
    """
    def logout(event):
        """
        Eventlistner for logout button
        """
        frm.destroy()
        main_frame()
        
    def back(event):
        """
        Eventlistner for back button
        """
        frm.destroy()
        welcome_admin_frame()
        
    def approve():
        """
        Function to approve posts posted by users which are unapproved
        """
        con=sqlite3.connect(database="database/city.sqlite")
        cursor=con.cursor()
        cursor.execute("update post set isApprove='yes' where isApprove='no'")
        con.commit()
        con.close()
        messagebox.showinfo("Approval","Post Approved")
        show_cat()
        frm.destroy()
        welcome_admin_frame()

    frm=Frame(win,bg="powder blue")
    frm.place(relx=.05,rely=.30,relwidth=.5,relheight=.6)
    
    frame_btn=Label(frm,image=imgtk_frame3,bg="black")
    frame_btn.place(relx=.0,rely=.0)
    
    lbl_wel=Label(frm,text="Welcome,Admin",fg='white',font=('Arial',12),bg="#51b7bb")
    lbl_wel.place(x=5,y=5)
    
    lbl_logout=Label(frm,image=imgtk_logout,bg='#76d4bc')
    lbl_logout.place(relx=.8,rely=.02)
    lbl_logout.bind("<Button>",logout)
    
    lbl_back=Label(frm,image=imgtk_back,bg="#51b7bb")
    lbl_back.place(relx=.02,y=25)
    lbl_back.bind("<Button>",back)
     
    st=ScrolledText(frm,height=18,width=70)
    st.place(relx=.05,rely=.15)
    st.insert("end","Category\t\tName\t\tAddress\t\tPosted By\n")
    st.insert("end","-------------------------------------------------------------------\n")
    
    con=sqlite3.connect(database="database/city.sqlite")
    cursor=con.cursor()
    cursor.execute("select * from post where isApprove='no'")
    info=""
    for row in cursor:
        info=info+"\n"+row[0]+"\t\t"+row[1]+"\t\t"+row[2]+"\t\t\t"+row[3]
        
    st.insert("end",info)
    
    btn_approve=Button(frm,text="approve",bd=5,command=approve)
    btn_approve.place(relx=.8,rely=.85)
    

def dlt_cat_frame():  
    """
    Function to delete particular category
    """
     
    def logout(event):
        """
        Eventlistner for logout button
        """
        frm.destroy()
        main_frame()
        
    def back(event):
        """
        Eventlistner for back button
        """
        frm.destroy()
        welcome_admin_frame()
        
    def dlt_db(event):
        """
        Eventlistner for delete category button
        """
        cat=e_cat.get()
        if(len(cat)==0):
            messagebox.showerror("Validation","Please enter category")
        else:
            try:
                con=sqlite3.connect(database="database/city.sqlite")
                cursor=con.cursor()
                cursor.execute("delete from category where cat_name=?",(cat.upper(),))
                con.commit()
                messagebox.showinfo("Category","category deleted")
                show_cat()
            except:
                messagebox.showerror("Category","category already deleted")
            con.close()
            
    
    frm=Frame(win,bg="powder blue")
    frm.place(relx=.05,rely=.30,relwidth=.5,relheight=.6)
    
    frame_btn=Label(frm,image=imgtk_frame3,bg="black")
    frame_btn.place(relx=.0,rely=.0)
    
    lbl_wel=Label(frm,text="Welcome,Admin",fg='white',font=('Arial',12),bg="#51b7bb")
    lbl_wel.place(x=5,y=5)
    
    lbl_logout=Label(frm,image=imgtk_logout,bg='#76d4bc')
    lbl_logout.place(relx=.8,rely=.02)
    lbl_logout.bind("<Button>",logout)
    
    lbl_back=Label(frm,image=imgtk_back,bg="#51b7bb")
    lbl_back.place(relx=.02,y=25)
    lbl_back.bind("<Button>",back)
    
    lbl_cat=Label(frm,text="Delete Category",font=('Arial',16),bg="#8ad5ba")
    lbl_cat.place(x=150,y=120)
    
    lbl_dlt=Label(frm,image=imgtk_dlt,bg='#c3dcbe')
    lbl_dlt.place(x=495,y=165)
    lbl_dlt.bind("<Button>",dlt_db)
    
    e_cat=Entry(frm,font=('Arial',16,'bold'),bd=4)
    e_cat.place(x=350,y=120)
    e_cat.focus()



# calling main frame function at startup
main_frame()

# calling mainloop method on win object to display Tkinter video
win.mainloop()