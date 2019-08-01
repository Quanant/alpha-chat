from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException
import time
from tkinter import *
from tkinter import messagebox as box
import sys
import PIL.Image
import PIL.ImageTk
import pickle
import requests

tk = Tk()
tk.title("Alpha Chat")
tk.iconbitmap('logo.ico')
canvas = Canvas(bd=0, highlightthickness=0)
canvas.pack_propagate(0)
canvas.pack(fill=BOTH, expand=1)
tk.state('zoomed')
canvas.config(bg='#fef9c7')
tk.minsize(662, 498)
tk.update()

im = PIL.Image.open("logo.png")
im = im.resize((100, 100), PIL.Image.ANTIALIAS)
logo = PIL.ImageTk.PhotoImage(im)

class User:
    def __init__(self, username):
        self.username = username
        self.channels = []

f = open("userInfo.dat",'rb')
mainUser = pickle.load(f)
f.close()

def setup():
    global channel
    channel = mainUser.channels[0]

def configWindow(event):
    height = canvas.winfo_height()
    width = canvas.winfo_width()
    msgEntry.configure(width=int(width/10.25))
    receiveBox.configure(width=int(width/10.25))
    receiveBox.configure(height=int(height/25))
    receiveBox.see(END)

receiveBox = Text(canvas, bg='#fef9c7', width=49, height=20, font='verdana 11', state=DISABLED, bd=0)
msgEntry = Entry(canvas, width=64, bg='#edeae5', font='verdana 11')
titleLabel = Label(canvas, image=logo, bg='#fef9c7')
userLabel = Label(canvas, bg='#fef9c7', font='verdana 11', text='Logged in as '+mainUser.username+'.')

# Need a subscribe listener
class SubListener(SubscribeCallback):
    def status(self, pubnub, status):
        pass
        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if status.operation == PNOperationType.PNSubscribeOperation or status.operation == PNOperationType.PNUnsubscribeOperation:
            if status.category == PNStatusCategory.PNConnectedCategory:
                pass
                # This is expected for a subscribe, this means there is no error or issue whatsoever
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # This usually occurs if subscribe temporarily fails but reconnects. This means
                # there was an error but there is no longer any issue
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                pass
                # This is the expected category for an unsubscribe. This means there
                # was no error in unsubscribing from everything
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass
                # This is usually an issue with the internet connection, this is an error, handle
                # appropriately retry will be called automatically
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # This means that PAM does not allow this client to subscribe to this
                # channel and channel group configuration. This is another explicit error
            else:
                pass
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult <link to the PNCONFIGURATION heartbeart config>
            if status.is_error():
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            pass
            # Encountered unknown status type
 
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def message(self, pubnub, message):
        receiveBox.config(state=NORMAL)
        receiveBox.insert(END, str(message.message)+'\n')
        receiveBox.see(END)
        receiveBox.config(state=DISABLED)

def handle_exception(e):
    print(e)

def sendMessage(*args):
    text = msgEntry.get()
    msgEntry.delete(0, len(text))
    msg = mainUser.username + ': ' + text
    pubnub.publish().channel(channel).message(msg).should_store(True).sync()

def closeProtocol():
    pubnub.unsubscribe_all()
    tk.destroy()
    sys.exit()

def history_callback(result, status):
    try:
        msgs = result.messages
        #start = result.start_timetoken
        #end = result.end_timetoken
        history = ''''''
        for i in msgs:
            history += str(i.entry) + '\n'
        receiveBox.config(state=NORMAL)
        receiveBox.insert(END, history)
        receiveBox.see(END)
        receiveBox.config(state=DISABLED)
        #envelope = pubnub.delete_messages() \
        #.channel(channel) \
        #.start(15640300853552356) \
        #.end(15645532511500479) \
        #.sync()
    except:
        pass

def mainScreen():
    try:
        requests.get('https://quanant.business.site/')
    except:
        box.showinfo('Network', 'Couldn\'t connect to the network. Please check your network connection, then restart the app.')
        tk.destroy()
    titleLabel.place(x=0, y=0)
    setup()
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = "sub-c-d7ac3638-ae96-11e9-b39e-aa7241355c4e"
    pnconfig.publish_key = "pub-c-416fd2e5-42a7-49f7-9952-fe8c5f13d25e"
    pnconfig.ssl = False
    pnconfig.uuid = mainUser.username

    global pubnub
    pubnub = PubNub(pnconfig)
    pubnub.add_listener(SubListener())
    pubnub.subscribe().channels(channel).execute()
    receiveBox.place(relx=0.007, rely=0.21)
    msgEntry.place(relx=0.015, rely=0.92)
    userLabel.place(relx=0.4, rely=0.05)
    msgEntry.bind("<Return>", sendMessage)
    history = pubnub.history().channel(channel).count(50).pn_async(history_callback)
    tk.protocol("WM_DELETE_WINDOW", closeProtocol)
    if len(mainUser.username) < 1 or len(mainUser.username) > 12:
        box.showinfo('Username', 'Please make your username between 1 and 12 characters long. You can do this in the Alpha Chat User Manager app.')
        tk.destroy()

try:
    mainScreen()
    configWindow(1)
    canvas.bind("<Configure>", configWindow)
    mainloop()
except:
    pass
