import pyttsx3
import webbrowser
import datetime as dt
import wikipedia
import pyjokes
import tkinter as tk
from tkinter import ttk, scrolledtext, font
import threading
from PIL import Image, ImageTk
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
        self.is_speaking = False
        
        # Setup GUI
        self.setup_gui()
        
        # Start with greeting
        self.clock()
        
    def setup_gui(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg=self.accent_color, height=80)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🤖 Voice Assistant",
            font=("Segoe UI", 24, "bold"),
            bg=self.accent_color,
            fg=self.fg_color
        )
        title_label.pack(expand=True)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Chat display area
        chat_frame = tk.Frame(main_container, bg=self.bg_color)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chat display with scrollbar
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Consolas", 11),
            bg="#0d0d1e",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for different message types
        self.chat_display.tag_config("assistant", foreground="#00ff41")
        self.chat_display.tag_config("user", foreground="#00b4d8")
        self.chat_display.tag_config("system", foreground="#ffb700")
        
        # Input frame
        input_frame = tk.Frame(main_container, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Input field
        self.input_field = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg="#0d0d1e",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            bd=10
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_field.bind("<Return>", lambda e: self.process_command())
        
        # Send button
        self.send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self.process_command,
            font=("Segoe UI", 11, "bold"),
            bg=self.hover_color,
            fg=self.fg_color,
            relief=tk.FLAT,
            padx=20,
            cursor="hand2"
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Quick action buttons frame
        button_frame = tk.Frame(main_container, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Quick action buttons
        quick_actions = [
            ("🌐 Google", lambda: self.execute_command("open google")),
            ("📹 YouTube", lambda: self.execute_command("open youtube")),
            ("✉️ Gmail", lambda: self.execute_command("open gmail")),
            ("🤖 ChatGPT", lambda: self.execute_command("open chatgpt")),
            ("🎮 Epic Games", lambda: self.execute_command("open epicgames")),
            ("🎮 Steam", lambda: self.execute_command("open steam")),
            ("🕐 Time", lambda: self.execute_command("time")),
            ("📅 Date", lambda: self.execute_command("date")),
            ("😂 Joke", lambda: self.execute_command("joke")),
            ("📜 History", lambda: self.execute_command("open history"))
        ]
        
        # Create two rows of buttons
        row1 = tk.Frame(button_frame, bg=self.bg_color)
        row1.pack(fill=tk.X, pady=(0, 5))
        row2 = tk.Frame(button_frame, bg=self.bg_color)
        row2.pack(fill=tk.X)
        
        for i, (text, command) in enumerate(quick_actions):
            target_row = row1 if i < 5 else row2
            btn = tk.Button(
                target_row,
                text=text,
                command=command,
                font=("Segoe UI", 10),
                bg=self.button_color,
                fg=self.fg_color,
                relief=tk.FLAT,
                padx=15,
                pady=8,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            # Bind hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.hover_color))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.button_color))
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=("Segoe UI", 10),
            bg=self.accent_color,
            fg=self.fg_color,
            anchor=tk.W,
            padx=10
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def speech(self, text):
        """Display and speak text"""
        self.display_message(f"Assistant: {text}", "assistant")
        self.update_status("Speaking...")
        
        # Run TTS in separate thread to prevent GUI freezing
        def speak_thread():
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False
            self.update_status("Ready")
            
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
        self.history(f"Voice Assistant: {text}")
        
    def clock(self):
        """Greet user based on time of day"""
        hr = int(dt.datetime.now().hour)
        if hr < 12:
            greeting = "Good Morning!"
        elif 12 <= hr < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        
        self.speech(greeting)
        self.speech("Hello, I am your voice Assistant. How can I help you!")
        
    def display_message(self, message, tag="user"):
        """Display message in chat window"""
        self.chat_display.insert(tk.END, message + "\n", tag)
        self.chat_display.see(tk.END)
        
    def update_status(self, status):
        """Update status bar"""
        self.status_bar.config(text=status)
        
    def process_command(self):
        """Process user input"""
        cmd = self.input_field.get().strip()
        if cmd:
            self.display_message(f"You: {cmd}", "user")
            self.input_field.delete(0, tk.END)
            self.history(f"You: {cmd}")
            
            # Process command in separate thread
            thread = threading.Thread(target=self.execute_command, args=(cmd,), daemon=True)
            thread.start()
            
    def execute_command(self, cmd):
        """Execute the given command"""
        cmd = cmd.lower()
        self.update_status("Processing...")
        
        if 'wikipedia' in cmd:
            self.speech("Searching Wikipedia...")
            search_term = cmd.replace("wikipedia", "").strip()
            try:
                res = wikipedia.summary(search_term, sentences=2)
                self.speech("According to Wikipedia")
                self.speech(res)
            except:
                self.speech("Sorry, I couldn't find any information on that topic.")
        
        elif 'open youtube' in cmd:
            webbrowser.open("www.youtube.com")
            self.speech("Opening YouTube")
            
        elif 'open google' in cmd:
            webbrowser.open("www.google.com")
            self.speech("Opening Google")
        
        elif 'open chatgpt' in cmd:
            webbrowser.open("www.chat.openai.com")
            self.speech("Opening ChatGPT")
            
        elif 'open epicgames' in cmd:
            webbrowser.open("www.epicgames.com")
            self.speech("Opening Epic Games")
            
        elif 'open gmail' in cmd:
            webbrowser.open("www.gmail.com")
            self.speech("Opening Gmail")
        
        elif 'open steam' in cmd:
            webbrowser.open("www.steampowered.com")
            self.speech("Opening Steam")
            
        elif 'time' in cmd:
            time = dt.datetime.now().strftime("%H:%M:%S")
            self.speech(f"The current time is {time}")
            
        elif 'date' in cmd:
            date = dt.datetime.now().strftime("%B %d, %Y")
            self.speech(f"Today's date is {date}")
            
        elif 'joke' in cmd:
            joke = pyjokes.get_joke()
            self.speech(joke)
        
        elif 'search' in cmd:
            search_query = cmd.replace("search", "").strip()
            if search_query:
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                self.speech(f"Searching for {search_query} on Google")
            else:
                self.speech("Please specify what you want to search for")
        
        elif 'exit' in cmd or 'quit' in cmd or 'stop' in cmd:
            self.speech("Goodbye! Have a great day.")
            self.root.after(2000, self.root.quit)  
            
        elif 'open history' in cmd:
            try:
                with open("history.txt", "r") as h:
                    history_content = h.read()
                    if history_content:
                        self.display_message("=== Command History ===", "system")
                        self.display_message(history_content, "system")
                        self.speech("Command history displayed")
                    else:
                        self.speech("History is empty")
            except FileNotFoundError:
                self.speech("No history file found")
                
        elif 'clear' in cmd or 'clear chat' in cmd:
            self.chat_display.delete(1.0, tk.END)
            self.speech("Chat cleared")
            
        else:
            self.speech("I didn't understand that command. Please try again.")
        
        self.update_status("Ready")
        
    def history(self, cmd):
        try:
            with open("history.txt", "a") as h:
                h.write(cmd + "\n")
        except:
            pass

def main():
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
