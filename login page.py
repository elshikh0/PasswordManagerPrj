from tkinter import *
from tkinter import messagebox
import ast
from PassMang import root_window
from db_operations import DbOperations
import bcrypt
import re





db_class = DbOperations()
db_class.create_table()

root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False,False)

def evaluate_password_strength(password):
    length_score = len(password) >= 8
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special_char = bool(re.search(r'[@$!%*?&^#]', password))
    score = sum([length_score, has_lowercase, has_uppercase,has_digit, has_special_char])

    if score == 5:
        return "Strong"
    elif score == 4:
        return "Medium"
    else:
        return "Weak"


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def check_password(stored_hash, entered_password):
    return bcrypt.checkpw(entered_password.encode(), stored_hash)



def signin():
    username = user.get()
    password = code.get()

    
    try:

        with open('datasheet.txt', 'r') as file:
              d = file.read()
              r = ast.literal_eval(d)
              file.close()

    

        if username in r.keys():
                stored_hash = r[username]

                if check_password(stored_hash, password):

                   root.destroy()
                   app_root = Tk()
                   app_root.title("Password Manager")
                   app = root_window(app_root, db_class)
                   app_root.mainloop()
        
                else :
                    messagebox.showerror("Invalid", "invalid username or password")
        else:
           messagebox.showerror("Invalid", "Invalid username or password")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def signup_command():
    window = Toplevel(root)

    window.title("SignUp")
    window.geometry('925x500+300+200')
    window.configure(bg='#fff')
    window.resizable(False,False)

    def password_strength_feedback():
        password = code.get()
        strength = evaluate_password_strength(password)
        strength_label.config(text=f"Password Strength: {strength}", fg="green" if strength == "Strong" else "orange" if strength == "Medium" else "red")

    def signup():
        username = user.get()
        password = code.get()
        confirm_password = confirm_code.get()

        if password == confirm_password:
            try:
                file = open('datasheet.txt', 'r+')
                d = file.read()
                r=ast.literal_eval(d)

                hashed_password = hash_password(password)

                dict2={username:hashed_password}
                r.update(dict2)
                file.truncate(0)
                file.close

                file = open('datasheet.txt', 'w')
                w = file.write(str(r))

                messagebox.showinfo('Sign Up', 'Successfully signed up')
                window.destroy()

            except:
                file = open('datasheet.txt', 'w')
                pp = str({username :hash_password(password)})
                file.write(pp)
                file.close()

        else:
                messagebox.showerror('Invalid', "Passwords didn't match")


    def sign():
        window.destroy()


    img = PhotoImage(file='signup.png')
    Label(window, image=img, border=0, bg='white').place(x=50, y=90)

    frame = Frame(window, width=350, height=390, bg='#fff')
    frame.place(x=480, y=50)


    heading= Label(frame, text='Sign Up', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light',23, 'bold'))
    heading.place(x=100,y=5)

    def on_enter(e):
        if user.get() == 'Username':
           user.delete(0, 'end')
    def on_leave(e):
        if user.get()=='':
            user.insert(0, 'Username')


    user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light',11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25,y=107)

    def on_enter(e):
        if code.get() == 'Password':
           code.delete(0, 'end')
        code.config(show="*")
    def on_leave(e):
        if code.get()=='':
            code.insert(0, 'Password')
            code.config(show="")


    code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light',11))
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)
    code.bind('<KeyRelease>', lambda e: password_strength_feedback())

    Frame(frame, width=295, height=2, bg='black').place(x=25,y=177)
    strength_label = Label(frame, text="Password Strength: ", fg="#57a1f8", bg="white", font=('Microsoft YaHei UI Light', 9))
    strength_label.place(x=30, y=250)

    def on_enter(e):
        if confirm_code.get() == 'Confirm Password':
           confirm_code.delete(0, 'end')
        confirm_code.config(show="*")
    def on_leave(e):
        if confirm_code.get()=='':
            confirm_code.insert(0, 'Confirm Password')
            confirm_code.config(show="")


    confirm_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light',11))
    confirm_code.place(x=30, y=220)
    confirm_code.insert(0, 'Confirm Password')
    confirm_code.bind('<FocusIn>', on_enter)
    confirm_code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25,y=247)


    Button(frame, width=39, pady=7, text='Sign Up', bg='#57a1f8', fg='white', border=0, command=signup).place(x=35, y=280)
    label = Label(frame, text='I have an account', fg='black', bg='white', font=('Microsoft YaHei UI Light',9))
    label.place(x=90,y=340)

    signin = Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=sign)
    signin.place(x=200,y=340)




    window.mainloop()



img = PhotoImage(file='login.png')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)


def on_enter(e):
    if user.get() == 'Username':
       user.delete(0,'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')


user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295,height=2, bg='black').place(x=25, y=107)


def on_enter(e):
    if code.get() == 'Password':
       code.delete(0,'end')
    code.config(show="*")

def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')
        code.config(show="")
        

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295,height=2, bg='black').place(x=25, y=177)


Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35,y=204)
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=signup_command)
sign_up.place(x=215,y=270)


root.mainloop()