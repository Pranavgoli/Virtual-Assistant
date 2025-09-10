# 🗣️ Python Voice Assistant  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange.svg)](https://github.com/yourusername/voice-assistant/pulls)  
[![Open Issues](https://img.shields.io/github/issues/yourusername/voice-assistant)](https://github.com/yourusername/voice-assistant/issues)  
[![Stars](https://img.shields.io/github/stars/yourusername/voice-assistant?style=social)](https://github.com/yourusername/voice-assistant/stargazers)  

A simple and interactive **Voice Assistant** built with Python.  
It can greet you, search Wikipedia, tell jokes, open websites, give the current time/date, and keep a history of your commands.  

------------------------

## ✨ Features  

- 🎙️ **Text-to-Speech (TTS)**: Speaks responses using `pyttsx3`.  
- ⏰ **Smart Greeting**: Greets you with "Good Morning", "Good Afternoon", or "Good Evening" based on the current time.  
- 🔎 **Wikipedia Search**: Fetches short summaries from Wikipedia.  
- 🌐 **Web Navigation**: Opens popular websites (YouTube, Google, ChatGPT, Gmail, Steam, Epic Games) or performs a custom **Google Search**.  
- 📅 **Time & Date**: Reads out the current time and today’s date.  
- 😂 **Fun Jokes**: Tells random programming jokes with `pyjokes`.  
- 📝 **History**: Saves all interactions in `history.txt`.  
- ❌ **Exit Anytime**: Type "exit", "quit", or "stop" to close the assistant.  

------------------------

## 📂 Project Structure  

  📁 VoiceAssistantProject
├── Voice_Assistant.py # Main assistant script
└── history.txt # Stores user and assistant interaction history

-----------------------

## 🔧 Installation  

1. Clone this repository:  

```bash
git clone https://github.com/Pranavgoli/Virtual-Assistant.git
cd voice-assistant

2. Install dependencies:

#  pip install pyttsx3 wikipedia pyjokes

#  webbrowser and datetime are built-in Python modules.
