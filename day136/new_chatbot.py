from tkinter import *


def send():
    send = "Kamu:" + e.get()
    text.insert(END, "\n" + send)
    if (e.get() == 'hi'):
        text.insert(END, "\n" + "Bot: hello")
    elif (e.get() == 'hello'):
        text.insert(END, "\n" + "Bot: hi")
    elif (e.get() == 'apa kabar?'):
        text.insert(END, "\n" + "Bot: baik, bagaimana denganmu?")
    elif (e.get() == 'tentu saja'):
        text.insert(END, "\n" + "Bot: senang berkenalan denganmu")
    elif (e.get() == 'makasih'):
        text.insert(END, "\n" + "Bot: sama-sama")
    elif (e.get() == 'bye'):
        text.insert(END, "\n" + "Bot: sampai-jumpa")
    else:
        text.insert(END, "\n" + "Bot: maaf, aku belum paham ucapanmu")


root = Tk()
text = Text(root, bg='light green')
text.grid(row=0, column=0, columnspan=2)
e = Entry(root, width=80)
send = Button(root, text='Send', bg='blue', width=20,
              command=send).grid(row=1, column=1)
e.grid(row=1, column=0)

root.title("Simple Chatbot")
root.mainloop()

# This designed followed itsourcecode.com
