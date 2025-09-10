import pyttsx3
import webbrowser
import datetime as dt
import wikipedia
import pyjokes

def speech(text):
    print(f"Voice Assistant: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    history(f"Voice Assistant: {text}")

def clock():
    hr = int(dt.datetime.now().hour)
    if hr < 12:
        speech("Good Morning!")
    elif hr > 12 and hr < 18:
        speech("Good Afternoon!")
    else:
        speech("Good Evening!")
    speech("Hello, I am your voice Assistant. How can I help you!")

def command():
    cmd = input("You (type your command): ").lower()
    history(f"You: {cmd}")
    return cmd

def run():
    clock()
    while True:
        cmd = command()
        if 'wikipedia' in cmd:
            speech("Searching Wikipedia...")
            cmd = cmd.replace("wikipedia","")
            try:
                res = wikipedia.summary(cmd, sentences = 2)
                speech("According to Wikipedia")
                speech(res)
            except:
                speech("Sorry, I couldn't find any information on that topic.")
        
        elif 'open youtube' in cmd:
            webbrowser.open("www.youtube.com")
            speech("Opening YouTube")

        elif 'open google' in cmd:
            webbrowser.open("www.google.com")
            speech("Opening Google")
        
        elif 'open chatgpt' in cmd:
            webbrowser.open("www.chat.openai.com")
            speech("Opening ChatGPT")

        elif 'open epicgames' in cmd:
            webbrowser.open("www.epicgames.com")
            speech("Opening Epic Games")

        elif 'open gmail' in cmd:
            webbrowser.open("www.gmail.com")
            speech("Opening Gmail")
        
        elif 'open steam' in cmd:
            webbrowser.open("www.steampowered.com")
            speech("Opening Steam")

        elif 'time' in cmd:
            time = dt.datetime.now().strftime("%H:%M:%S")
            speech("The current time is ")
            speech(time)

        elif 'date' in cmd:
            date = dt.datetime.now().strftime("%B %d, %Y")
            speech("Today's date is ")
            speech(date)

        elif 'joke' in cmd:
            joke = pyjokes.get_joke()
            speech(joke)
        
        elif 'search' in cmd:
            cmd = cmd.replace("search","")
            webbrowser.open(f"https://www.google.com/search?q={cmd}")
            speech(f"Searching for {cmd} on Google")
        
        elif 'exit' in cmd or 'quit' in cmd or 'stop' in cmd:
            speech("Goodbye! Have a great day.")
            break

        elif 'open history' in cmd:
            with open("history.txt","r") as h:
                speech("Here is your command history:")
                speech(h.readline())

        else:
            speech("I didn't understand that command. Please try again.")
        
def history(cmd):
    with open("history.txt","a") as h:
        h.write(cmd + "\n")

if __name__ == "__main__":
    run()