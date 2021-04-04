from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from tkinter import *
import pyttsx3 as pp
import speech_recognition as s
import threading

engine = pp.init()

# Import the logic for talking and listening
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[0].id)


# A function for the chatbot to read its responce
def speak(words):
    engine.say(words)
    engine.runAndWait()


# Chatbot logic
# pyttsx3
bot = ChatBot("Chat Bot")

# Read the training file with the responses
# chat = open('train//train.yml', 'r').readlines()
chat = open('chat.txt', 'r').readlines()

# Define the trainer for the Chatbot
trainer = ListTrainer(bot)

# Train the Chatbot
trainer.train(chat)

# Interface part with TKINTER
window = Tk()
window.geometry("500x500")  # Window dimensions
window.title("Chat Bot")  # Title of the window
logo = PhotoImage(file="CvijaLogo.PNG")
logopic = Label(window, image=logo)  # Logo in the chatbot window
logopic.pack(pady=5)
window.configure(bg='#856ff8')


# TakeY query takse the audio as input from the user and converts it to string
def takeQuery():
    speach_rec = s.Recognizer()
    speach_rec.pause_threshold = 1
    print("Your bot is listening try to speak.")
    with s.Microphone() as m:
        try:
            audio = speach_rec.listen(m)
            query = speach_rec.recognize_google(audio, language='eng-in')
            print(query)
            textF.delete(0, END)
            textF.insert(0, query)
            ask_from_bot()
        except Exception as e:
            print(e)
            print("not recognized")


# Get answer from the chatbot
def ask_from_bot():
    query = textF.get()
    Chatbot_answer = bot.get_response(query)
    msgs.insert(END, "You : " + query)
    print(type(Chatbot_answer))
    msgs.insert(END, "Bot : " + str(Chatbot_answer))
    speak(Chatbot_answer)
    textF.delete(0, END)
    msgs.yview(END)


inside_window = Frame(window)

sc = Scrollbar(inside_window)  # Scrollbar
msgs = Listbox(inside_window, width=75, height=15,
               yscrollcommand=sc.set)  # Box where all the messages are visible historically
sc.pack(side=RIGHT, fill=Y)  # Position the scrollbar
msgs.pack(side=LEFT, fill=BOTH, pady=10)  # Position the history message box

inside_window.pack()

# Input text field
textF = Entry(window, font=("Courier", 10), width=75)
textF.pack(fill=X, pady=10, padx=15)

# Defined button
btn = Button(window, text="Ask Chat Bot", font=("Courier", 10), fg='white', bg='green', command=ask_from_bot)
btn.pack()


# creating a function
def enter_function(event):
    btn.invoke()


# going to bind window window with enter key...
window.bind('<Return>', enter_function)


def repeatL():
    while True:
        takeQuery()


t = threading.Thread(target=repeatL)

t.start()

window.mainloop()