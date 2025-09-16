import pyttsx3
import webbrowser
import datetime as dt
import wikipedia
import pyjokes
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
import os

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("900x700")
        
        # Set color scheme
        self.bg_color = "#1a1a2e"
        self.fg_color = "#eee"
        self.accent_color = "#0f3460"
        self.button_color = "#16213e"
        self.hover_color = "#e94560"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize TTS engine
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        
        # TTS queue
        self.tts_queue = queue.Queue()
        self.is_speaking = False
        
        # Setup GUI
        self.setup_gui()
        
        # Start TTS worker
        self.start_tts_worker()
        
        # Greeting
        self.root.after(100, self.clock)
    
    def setup_gui(self):
        # Title
        title_frame = tk.Frame(self.root, bg=self.accent_color, height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, text="🤖 Voice Assistant",
            font=("Segoe UI", 24, "bold"), bg=self.accent_color, fg=self.fg_color
        )
        title_label.pack(expand=True)
        
        # Chat display
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        chat_frame = tk.Frame(main_container, bg=self.bg_color)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, width=70, height=20,
            font=("Consolas", 11), bg="#0d0d1e", fg=self.fg_color,
            insertbackground=self.fg_color, relief=tk.FLAT, padx=10, pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Chat tags (colors)
        self.chat_display.tag_config("assistant", foreground="white", background="#238636", spacing3=5, lmargin1=10, lmargin2=10, rmargin=5)
        self.chat_display.tag_config("user", foreground="white", background="#1f6feb", spacing3=5, lmargin1=5, lmargin2=5, rmargin=10)
        self.chat_display.tag_config("system", foreground="#ffb700")
        
        # Input
        input_frame = tk.Frame(main_container, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.input_field = tk.Entry(
            input_frame, font=("Segoe UI", 12), bg="#0d0d1e", fg=self.fg_color,
            insertbackground=self.fg_color, relief=tk.FLAT, bd=10
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_field.bind("<Return>", lambda e: self.process_command())
        
        self.send_btn = tk.Button(
            input_frame, text="Send", command=self.process_command,
            font=("Segoe UI", 11, "bold"), bg=self.hover_color, fg=self.fg_color,
            relief=tk.FLAT, padx=20, cursor="hand2"
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Quick actions
        button_frame = tk.Frame(main_container, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        quick_actions = [
            ("🌐 Google", lambda: self.quick_command("open google")),
            ("📹 YouTube", lambda: self.quick_command("open youtube")),
            ("✉️ Gmail", lambda: self.quick_command("open gmail")),
            ("🤖 ChatGPT", lambda: self.quick_command("open chatgpt")),
            ("🎮 Epic Games", lambda: self.quick_command("open epicgames")),
            ("🎮 Steam", lambda: self.quick_command("open steam")),
            ("🕐 Time", lambda: self.quick_command("time")),
            ("📅 Date", lambda: self.quick_command("date")),
            ("😂 Joke", lambda: self.quick_command("joke")),
            ("📜 History", lambda: self.quick_command("open history"))
        ]
        
        for i, (text, command) in enumerate(quick_actions):
            btn = tk.Button(
                button_frame, text=text, command=command,
                font=("Segoe UI", 10), bg=self.button_color, fg=self.fg_color,
                relief=tk.FLAT, padx=15, pady=8, cursor="hand2"
            )
            btn.grid(row=i//5, column=i%5, padx=3, pady=3, sticky="nsew")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.hover_color))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.button_color))
        
        # Equal expand for buttons
        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root, text="Ready", font=("Segoe UI", 10),
            bg=self.accent_color, fg=self.fg_color, anchor=tk.W, padx=10
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def start_tts_worker(self):
        def tts_worker():
            while True:
                try:
                    text = self.tts_queue.get()
                    if text is None:
                        break
                    self.is_speaking = True
                    self.update_status("Speaking...")
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.is_speaking = False
                    self.update_status("Ready")
                except Exception as e:
                    print(f"TTS Error: {e}")
                    self.is_speaking = False
                    self.update_status("Ready")
        threading.Thread(target=tts_worker, daemon=True).start()
    
    def speech(self, text):
        """Thread-safe speech"""
        def _speak():
            self.display_message(f"Assistant: {text}", "assistant")
            self.tts_queue.put(text)
            self.history(f"Voice Assistant: {text}")
        self.root.after(0, _speak)
    
    def clock(self):
        hr = int(dt.datetime.now().hour)
        if hr < 12:
            greeting = "Good Morning!"
        elif 12 <= hr < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        
        self.speech(greeting)
        self.root.after(700, lambda: self.speech("Hello, I am your voice Assistant. How can I help you!"))
    
    def display_message(self, message, tag="user"):
        self.chat_display.insert(tk.END, message + "\n\n", tag)
        self.chat_display.see(tk.END)
    
    def update_status(self, status):
        self.root.after(0, lambda: self.status_bar.config(text=status))
    
    def quick_command(self, cmd):
        self.display_message(f"You: {cmd}", "user")
        self.history(f"You: {cmd}")
        threading.Thread(target=self.execute_command, args=(cmd,), daemon=True).start()
    
    def process_command(self):
        cmd = self.input_field.get().strip()
        if cmd:
            self.display_message(f"You: {cmd}", "user")
            self.input_field.delete(0, tk.END)
            self.history(f"You: {cmd}")
            threading.Thread(target=self.execute_command, args=(cmd,), daemon=True).start()
    
    def execute_command(self, cmd):
        cmd = cmd.lower()
        self.update_status("Processing...")
        try:
            if 'wikipedia' in cmd:
                self.speech("Searching Wikipedia...")
                search_term = cmd.replace("wikipedia", "").strip()
                if search_term:
                    try:
                        res = wikipedia.summary(search_term, sentences=2)
                        self.speech("According to Wikipedia")
                        self.root.after(700, lambda: self.speech(res))
                    except wikipedia.exceptions.DisambiguationError as e:
                        self.speech(f"Multiple results found: {', '.join(e.options[:3])}")
                    except wikipedia.exceptions.PageError:
                        self.speech("Sorry, no Wikipedia page found.")
                else:
                    self.speech("Please specify what to search on Wikipedia.")
            
            elif 'open youtube' in cmd:
                webbrowser.open("https://www.youtube.com")
                self.speech("Opening YouTube")
            
            elif 'open google' in cmd:
                webbrowser.open("https://www.google.com")
                self.speech("Opening Google")
            
            elif 'open chatgpt' in cmd:
                webbrowser.open("https://chat.openai.com")
                self.speech("Opening ChatGPT")
            
            elif 'open epicgames' in cmd:
                webbrowser.open("https://www.epicgames.com")
                self.speech("Opening Epic Games")
            
            elif 'open gmail' in cmd:
                webbrowser.open("https://mail.google.com")
                self.speech("Opening Gmail")
            
            elif 'open steam' in cmd:
                webbrowser.open("https://store.steampowered.com")
                self.speech("Opening Steam")
            
            elif 'time' in cmd:
                current_time = dt.datetime.now().strftime("%I:%M %p")
                self.speech(f"The current time is {current_time}")
            
            elif 'date' in cmd:
                current_date = dt.datetime.now().strftime("%B %d, %Y")
                day = dt.datetime.now().strftime("%A")
                self.speech(f"Today is {day}, {current_date}")
            
            elif 'joke' in cmd:
                self.speech("Here's a joke for you:")
                self.root.after(700, lambda: self.speech(pyjokes.get_joke()))
            
            elif 'search' in cmd:
                query = cmd.replace("search", "").strip()
                if query:
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                    self.speech(f"Searching Google for {query}")
                else:
                    self.speech("Please specify what you want to search.")
            
            elif 'exit' in cmd or 'quit' in cmd:
                self.speech("Goodbye! Have a great day.")
                self.root.after(2500, self.close_application)
            
            elif 'open history' in cmd:
                try:
                    with open("history.txt", "r") as h:
                        content = h.read().strip()
                        if content:
                            self.display_message("=== Command History ===", "system")
                            self.display_message("\n".join(content.split("\n")[-20:]), "system")
                            self.speech("Command history displayed")
                        else:
                            self.speech("History is empty.")
                except FileNotFoundError:
                    self.speech("No history file found yet.")
            
            elif 'clear' in cmd:
                self.chat_display.delete(1.0, tk.END)
                self.speech("Chat cleared")
            
            elif 'help' in cmd:
                help_text = """Available commands:
- open google/youtube/gmail/chatgpt/steam/epicgames
- wikipedia [topic]
- search [query]
- time / date
- joke
- clear chat
- show history
- exit/quit"""
                self.display_message(help_text, "system")
                self.speech("Help menu displayed in chat")
            
            else:
                self.speech("I didn't understand that. Type 'help' to see available commands.")
        
        except Exception as e:
            print(f"Command error: {e}")
            self.speech("Sorry, I encountered an error.")
        
        self.update_status("Ready")
    
    def close_application(self):
        self.tts_queue.put(None)
        self.root.quit()
    
    def history(self, cmd):
        try:
            ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("history.txt", "a", encoding="utf-8") as h:
                h.write(f"[{ts}] {cmd}\n")
        except Exception as e:
            print(f"History save error: {e}")

def main():
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.protocol("WM_DELETE_WINDOW", lambda: app.close_application())
    root.mainloop()

if __name__ == "__main__":
    main()
