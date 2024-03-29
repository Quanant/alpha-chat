import pickle
from tkinter import *
from tkinter import messagebox as box
import PIL.Image
import PIL.ImageTk

tk = Tk()
tk.title("Alpha Chat User Manager")
tk.iconbitmap('userLogo.ico')
tk.resizable(0, 0)
canvas = Canvas(bd=0, highlightthickness=0, width=400, height=300)
canvas.pack()
canvas.config(bg='#fef9c7')
tk.update()

im = PIL.Image.open("logo.png")
im = im.resize((100, 100), PIL.Image.ANTIALIAS)
logo = PIL.ImageTk.PhotoImage(im)

class User:
    def __init__(self, username):
        self.username = username
        self.channels = ["RegRoom"]

user = User(None)

def dump(*args):
    user.username = userEntry.get()
    f = open("userInfo.dat", "wb")
    pickle.dump(user, f)
    f.close()
    userEntry.delete(0, END)
    box.showinfo('Username', 'Your username has been updated to "'+user.username+'".')

titleLabel = Label(canvas, image=logo, bg='#fef9c7')
userLabel = Label(canvas, text='Username:', bg='#fef9c7', font='verdana 20')
userEntry = Entry(canvas, width=38, font='verdana 11', bg='#edeae5')
goButton = Button(canvas, text="Update Username", command=dump, bg='#edeae5', font='verdana 14')
userLabel.place(relx=0.33, rely=0.3)
titleLabel.place(relx=0, rely=0)
userEntry.place(relx=0.02, rely=0.45)
goButton.place(relx=0.27, rely=0.7)

mainloop()
