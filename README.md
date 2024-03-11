# Whisper Transcribe Directory
This script transcribes audio and video files in a specified directory, including subdirectories, using OpenAI's Whisper models. It allows for model selection to balance between speed and accuracy based on user requirements.

# Requirements
Python 3.8+
Whisper
Tkinter (usually included with Python)
FFmpeg

# Setup
Install Whisper: pip install git+https://github.com/openai/whisper.git
Ensure FFmpeg is installed on your system.

# Usage
Run transcribe.py and follow the prompts to select a directory and a Whisper model. The script will transcribe all supported files in the directory and its subdirectories, saving the transcriptions as .txt files.

