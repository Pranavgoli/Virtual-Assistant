🤖 Voice Assistant with GUI
A modern, feature-rich voice assistant with a sleek graphical user interface built using Python. This assistant can perform various tasks including web searches, opening websites, telling jokes, and providing time/date information, all while speaking responses aloud.

=========================================================================================================

✨ Features
🎯 Core Functionality

Voice Output: Text-to-speech capabilities for all responses
Wikipedia Integration: Quick Wikipedia searches and summaries
Web Browser Control: Open popular websites with simple commands
Google Search: Perform Google searches directly from the assistant
Time & Date: Get current time and date information
Jokes: Lighten the mood with programming and general jokes
Command History: Track all your interactions with the assistant

🎨 GUI Features

Modern Dark Theme: Eye-friendly dark interface
Real-time Chat Display: Color-coded message history
Quick Action Buttons: One-click access to common commands
Responsive Design: Non-blocking UI with threaded operations
Status Indicators: Visual feedback for assistant actions

=========================================================================================================

🚀 Quick Start
Prerequisites
Ensure you have Python 3.7 or higher installed on your system.

Installation
Clone the repository:

                    git clone https://github.com/yourusername/voice-assistant-gui.git
                    cd voice-assistant-gui

Install required dependencies:

                    pip install -r requirements.txt

Or install packages individually:

                    pip install pyttsx3 wikipedia pyjokes pillow

Running the Application:

                    python Voice_Assistant.py

📋 Requirements
Create a requirements.txt file with:

                    pyttsx3>=2.90
                    wikipedia-api>=0.5.4
                    pyjokes>=0.6.0
                    pillow>=9.0.0

Quick Action Buttons
The GUI includes quick action buttons for frequently used commands:

🌐 Google
📹 YouTube
✉️ Gmail
🤖 ChatGPT
🎮 Epic Games
🎮 Steam
🕐 Time
📅 Date
😂 Joke
📜 History

🏗️ Project Structure:

                     voice-assistant-gui/
                     │
                     ├── voice_assistant_gui.py    # Main application file with GUI
                     ├── history.txt               # Command history (auto-generated)
                     ├── requirements.txt          # Python dependencies
                     ├── README.md                # Project documentation
                     └── LICENSE                  # License file

🐛 Known Issues:

TTS might not work on some Linux distributions without additional configuration
Some websites may not open correctly if the URL protocol is missing
Wikipedia searches may fail for ambiguous terms

📈 Future Enhancements:

🎤 Voice input recognition
🔊 Volume control for TTS
🌐 Multi-language support
📱 Mobile app version
☁️ Cloud sync for history
🤖 AI-powered responses
📊 Usage analytics dashboard

🙏 Acknowledgments:

pyttsx3 for text-to-speech functionality
Wikipedia-API for Wikipedia integration
pyjokes for the jokes database
Tkinter for the GUI framework

📝 License:

This project is licensed under the MIT License - see the LICENSE file for details.
