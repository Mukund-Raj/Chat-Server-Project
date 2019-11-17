from tkinter import *
from tkinter import messagebox
from tkinter import ttk as tk
import socket
from threading import Thread
import json
spmessagenotfound="notfound404"

fontt="Verdana"
'''style=Style()
style.map("mybutton",relief=GROOVE,background=[('pressed', '!disabled', '#CCCCFF'), ('active', '#99FFFF')])
'''
#---------------------------------------------------------------------------------------------------------------------#
def Send(my_msg):
    print("message sent!!!")
    pos_scroll=vsb.get()[1]
    textarea.config(state=NORMAL)
    msg=my_msg
    b=bool(msg.strip())
    
    if b:
        textarea.insert(END,"\n")

    textarea.config(state=DISABLED)
    if(pos_scroll==1):
        textarea.yview_moveto(1)
    print("b=",b)

    d={}
    if '=' in my_msg:
        li=my_msg.split('=')
        print(li[0])
        d[li[0]]=li[1]
        message=json.dumps(d)
    else:
        d["all"]=my_msg
        message=json.dumps(d)
        print(d)
    if b:
        Client_socket.send(bytes(message,'utf-8'))
    if my_msg=="good bye":
        #Client_socket.send(bytes("good bye", "utf8"))
        Client_socket.close()
        messagebox.showinfo("Info","Apllication is quitting")
        f.close()
        root.destroy() 

#---------------------------------------------------------------------------------------------------------------------#
#for handling received messages
def Receive():
    '''
    fr=open('chatfile.txt','r')
    for x in fr:
        pos_scroll=vsb.get()[1]
        textarea.config(state=NORMAL)
        textarea.insert(END,"\n")
        textarea.insert(END,x)
        textarea.config(state=DISABLED)
        if(pos_scroll==1):
            textarea.yview_moveto(1) 
    fr.close()
    '''
    while True:
        try:
            recv_data=Client_socket.recv(2048).decode('utf-8')
            recv_data=str(recv_data)
            print("server:"+recv_data)
            pos_scroll=vsb.get()[1]
            textarea.config(state=NORMAL)
            textarea.insert(END,"\n")
            text=recv_data
            f.write(text)
            f.write('\n')
            textarea.insert(END,text)
            textarea.config(state=DISABLED)
            if(pos_scroll==1):
                textarea.yview_moveto(1) 
        except OSError:
            break

def on_message_sent(event=None):
    message=entry.get()
    entry.delete(0,END)
    Send(message)
    

def when_closing():
    msg="good bye"
    result=messagebox.askyesno("Quit","Do you want to quit?")
    print(result)
    if result==True:
        Send(msg) 
        #root.destroy()
        f.close()
        
#---------------------------------------------------------------------------------------------------------------------#

def loginpage():
    login=Tk()
    login.lift()
    login.attributes("-topmost",True)
    
    #logf=Frame(login)
    Top = Frame(login, bd=2,  relief=RIDGE)
    Top.pack(side=TOP, fill=X)
    
    logininfo=Frame(login)
    logininfo.pack(side=TOP,fill=X)
    
    f1 = Frame(login, height=200)
    f1.pack(side=TOP, pady=20)
    
    login.focus_force()
    
    infolabel=Label(Top,text="Welcome to the chat",font=('verdana',18))
    infolabel.pack(fill=X)

    loginlabel=Label(logininfo,text="LOGIN",font=('cambria',18))
    loginlabel.pack(fill=X)
    userlabel=Label(f1,text="Username:",padx=5,pady=5,font=(14))
    userlabel.grid(row=0,column=0)
    
    username=Entry(f1,textvariable=USER,font=(14),width=18)
    username.grid(row=0,column=1)
    username.focus()
    passwordlabel=Label(f1,text="Password:",padx=5,pady=5,font=(14))
    passwordlabel.grid(row=1,column=0)

    Password=Entry(f1,textvariable=PASSWORD,show="*",font=(14),width=18)
    Password.grid(row=1,column=1)
    
    logb=Button(f1,text="Login",font=(14),fg="black",bg="lightblue",relief=GROOVE,command=lambda:details(username.get(),Password.get(),login))
    logb.grid(row=2,column=0,ipadx=1)
    login.focus_set()
    #login.tk_focusFollowsMouse()
    newuser=Button(f1,text="New User",font=(14),fg="black",bg="lightblue",relief=GROOVE,command=lambda:newUser(login))
    newuser.grid(row=2,column=1,ipadx=2)

def newUser(loginwindow):
    loginwindow.destroy()

    login=Tk()
    login.lift()
    login.attributes("-topmost",True)
    
    #logf=Frame(login)
    Top = Frame(login, bd=2,  relief=RIDGE)
    Top.pack(side=TOP, fill=X)
    
    logininfo=Frame(login)
    logininfo.pack(side=TOP,fill=X)
    
    f1 = Frame(login, height=200)
    f1.pack(side=TOP, pady=20)
    
    login.focus_force()
    
    infolabel=Label(Top,text="Welcome to the chat",font=('verdana',18))
    infolabel.pack(fill=X)

    loginlabel=Label(logininfo,text="New User Registration",font=('cambria',18))
    loginlabel.pack(fill=X)
    userlabel=Label(f1,text="Username:",padx=5,pady=5,font=(14))
    userlabel.grid(row=0,column=0)
    
    username=Entry(f1,textvariable=USER,font=(14),width=18)
    username.grid(row=0,column=1)
    username.focus()
    passwordlabel=Label(f1,text="Password:",padx=5,pady=5,font=(14))
    passwordlabel.grid(row=1,column=0)

    Password=Entry(f1,textvariable=PASSWORD,show="*",font=(14),width=18)
    Password.grid(row=1,column=1)
    
    
    login.focus_set()
    logb=Button(f1,text="create account",font=(14),fg="black",bg="lightblue",relief=GROOVE,command=lambda:newaccount(username.get(),Password.get(),login))
    logb.grid(row=2,column=0,ipadx=1)
    login.focus_set()
    #login.tk_focusFollowsMouse()
    msg="newuser"+"="+"password101"
    Send(msg)

def newaccount(username,password,newuserwindow):
    newUser={}
    
    if username!=''  and password!='':
        print("working")
        newUser[username]=password
        h=json.dumps(newUser)
        Client_socket.send(bytes(h,'utf-8'))
        name_info=Client_socket.recv(1024).decode('utf-8')
    else:
        name_info="401"

    if name_info=="401":
        messagebox.showinfo("info","Fields are required")
    else:
        
        if(name_info=="405"):
            #username.set('')
            messagebox.showinfo("info","username taken,enter something else")
        else:
            root.deiconify()
            receive_thread = Thread(target=Receive)
            receive_thread.start()
            newuserwindow.destroy()
        

def details(name,password,login):
    if name!='' and password!='':
        msg=name+"="+password
        print(msg)
        Send(msg)
        loginreceive(login)
    else:
        messagebox.showinfo("info","Fields are required") 

def loginreceive(login):
    logindata=Client_socket.recv(1024).decode('utf-8')
    print(logindata)
    logindata=str(logindata)
    if(logindata!=spmessagenotfound):
        print("true found")
        receive_thread = Thread(target=Receive)
        receive_thread.start()
        login.destroy()
        root.deiconify()
        
    else:
        messagebox.showinfo("Error","wrong ID or password")
            


if __name__ == "__main__":
    Client_socket=socket.socket()
    host=socket.gethostname()
    port=65100
  
    Client_socket.connect((host,port))
    root=Tk()
    USER=StringVar()
    PASSWORD=StringVar()
    s=tk.Style()
    print(s.theme_names())
    s.theme_use('winnative')
    root.wm_iconbitmap('message1.ico')
    root.title("Chat window")
    interior=Frame(root)
    #root.configure(background="red")
    tk.Style().configure("TButton", padding=5, relief=RAISED,background="blue")
    interior.pack(expand=True,fill=BOTH)
    top_frame=Frame(interior)
    top_frame.pack(expand=True,fill=BOTH)
    
    
    textarea=Text(top_frame,state=DISABLED,font=(fontt,"13"))
    vsb=Scrollbar(top_frame,takefocus=0,command=textarea.yview)
    vsb.pack(side=RIGHT,fill=Y)
    textarea.pack(side=RIGHT,expand=True,fill=BOTH)
    textarea["yscrollcommand"]=vsb.set
    entry_frame=tk.Frame(interior)
    entry_frame.pack(fill=X,anchor=N)
    #entry_label=Label(entry_frame)
    entry=Entry(entry_frame,bd=3,relief=GROOVE,font=(fontt,"10"))
    entry.pack(side=LEFT,expand=True,fill=X)
    entry.bind("<Return>",on_message_sent)
    entry.focus()
    label=tk.Label(entry_frame,text="You:",padding=5,background="#AFDBF5",relief=GROOVE)
    label.pack(side=LEFT,before=entry)
    style = tk.Style()
    style.map("C.TButton",
        foreground=[('pressed', '#AFDBF5'), ('active', 'blue')],
        background=[('pressed', '!disabled', 'black'), ('active', 'white')]
        )
    send_button = tk.Button(entry_frame, text=" Send ",style="C.TButton",command=on_message_sent)
    send_button.pack(side=RIGHT,padx=5, after=entry)
    root.withdraw()
    root.protocol("WM_DELETE_WINDOW",when_closing)
    f=open('chatfile.txt','a')
    
    root.withdraw()
    loginpage()
    root.mainloop()
