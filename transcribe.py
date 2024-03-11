import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from whisper import load_model


whisper_models = {
    "tiny": "Fastest model, minimal hardware requirements, suitable for quick tasks.",
    "small": "Mid-sized model, improved accuracy for complex audio, requires moderate hardware.",
    "base": "Balances speed and accuracy, suitable for general use with limited resources.",
    "medium": "Large model, high accuracy for detailed tasks, requires significant hardware.",
    "large": "Largest model, highest accuracy, ideal for challenging audio, demands substantial hardware resources.",
    "tiny.en": "English-optimized version of the tiny model, offering better performance for English audio.",
    "small.en": "English-optimized version of the small model, enhanced for English audio tasks.",
    "base.en": "English-optimized version of the base model, improving performance for English audio.",
    "medium.en": "English-optimized version of the medium model, best for English audio with high accuracy needs."
}



def choose_directory():
    # Initialize the Tkinter root element
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # Open a dialog window for choosing a directory
    directory_path = filedialog.askdirectory(initialdir=desktop_path)
    return directory_path

def transcribe_file(file_path, model_name):
    model = load_model(model_name)  # Using the base model for demonstration; adjust as needed
    result = model.transcribe(file_path, verbose=True, fp16=False, task="transcribe")
    return result['text']


# Define a list of transcribable file extensions
transcribable_extensions = ['.mp3', '.wav', '.m4a', '.mp4', '.mkv', '.avi']


def choose_model(models):
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Select a Model")

    # Create a Combobox for model selection
    tk.ttk.Label(root, text="Choose a Whisper model:").grid(column=0, row=0, padx=10, pady=10)
    selected_model = tk.StringVar()
    model_selector = tk.ttk.Combobox(root, width=60, textvariable=selected_model, state="readonly")
    model_selector['values'] = list(models.keys())  # Use the keys of the dictionary as values
    model_selector.grid(column=0, row=1, padx=10, pady=10)
    model_selector.current(7)  # Set the default selection on base.en

    # Function to handle "OK" button click
    def on_ok_clicked():        
        root.quit()


    # OK button
    ok_button = tk.ttk.Button(root, text="OK", command=on_ok_clicked)
    ok_button.grid(column=0, row=2, padx=10, pady=10)

    # Display the models and their descriptions
    for i, (model, description) in enumerate(models.items()):
        tk.Label(root, text=f"{model}: {description}").grid(column=1, row=i, padx=10, pady=5)

    root.mainloop()  # Run the Tkinter event loop

    chosen_model = model_selector.get()  # Assign the value of selected_model.get() to a variable
    print(f"Selected model: {chosen_model}")
    root.withdraw() 
    return chosen_model



# Function to list transcribable files in a directory
def list_transcribable_files(directory):
    transcribable_files = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has a transcribable extension
            if any(file.lower().endswith(ext) for ext in transcribable_extensions):
                # Add the file to the list
                transcribable_files.append(os.path.join(root, file))

    return transcribable_files

# Specify the directory to check
directory_to_check = choose_directory()

# Get the list of transcribable files
files_to_transcribe = list_transcribable_files(directory_to_check)

# Print the list of files
print("Files that can be transcribed:")
for file in files_to_transcribe:
    print(file)

selected_model = choose_model(whisper_models)  # Let the user choose a model
print (f"Using model: {selected_model}")

# Transcribe the files to a text file if the text file with the same name is absent
# or is empty. 
    
for file in files_to_transcribe:
    print(f"Transcribing {file}...")

    print(f"File path being transcribed: '{file}'")

    # Check if the text file already exists
    text_file = os.path.splitext(file)[0] + ".txt"
    if os.path.exists(text_file) and os.path.getsize(text_file) > 0:
        print(f"Skipping {text_file} because it already exists and is not empty")
        continue

    transcribed_text = transcribe_file(file, model_name=selected_model)

    # Check if the transcribed text is empty
    if not transcribed_text:
        continue


    # Write the transcribed text to the text file
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(transcribed_text)


    print(f"Transcribed text written to {text_file}")

    print()

