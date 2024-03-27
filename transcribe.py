import os
import tkinter as tk
from tkinter import filedialog, ttk
from whisper import load_model, transcribe, available_models
from whisper.utils import get_writer
import time
import json
from langdetect import detect  

output_formats = ['txt', 'srt', 'vtt', 'tsv', 'json']

LANGUAGES = {
    "None": "find out automatically",
    "it": "italian",
    "en": "english",
    "zh": "chinese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
    "yue": "cantonese",
}

def invert_dict(d):
    return dict((v, k) for k, v in d.items())

LANGUAGES_CODES = invert_dict(LANGUAGES)


# Define a list of transcribable file extensions
transcribable_extensions = ['.mp3', '.wav', '.m4a', '.mp4', '.mkv', '.avi']
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

def is_old_json_format(data):
    # Check if the data is in the old JSON format
    if not isinstance(data, list):      return False
    if not isinstance(data[0], dict):   return False
    if not "text" in data[0]:           return False
    return True

def is_new_json_format(data):
    # Check if the data is in the new JSON format
    if not isinstance(data, dict):       return False
    if not "text" in data:               return False
    return True

def infer_language_from_text(text):
    return detect(text)

def is_file_locked(file_path):
    lock_file = file_path + ".lock"

    # Check if the lock file exists
    if os.path.exists(lock_file):
        # Check the age of the lock file
        lock_age = time.time() - os.path.getmtime(lock_file)
        if lock_age > 7200:  # 2 hours in seconds
            os.remove(lock_file)  # Remove stale lock
            return False  # File was locked, but lock was stale
        else:
            return True  # File is actively locked
    return False  # No lock exists

def unlock_file(file_path):
    lock_file = file_path + ".lock"
    try:
        os.remove(lock_file)  # Remove the lock file
    except FileNotFoundError:
        pass

def choose_directory():
    # Initialize the Tkinter root element
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # Open a dialog window for choosing a directory
    directory_path = filedialog.askdirectory(initialdir=desktop_path)
    return directory_path

def transcribe_file(file_path, model_name,prompt_to_send="",selected_language_code="None"):
    model = load_model(model_name)  # Using the base model for demonstration; adjust as needed
    result = model.transcribe(file_path, verbose=True, fp16=False, task="transcribe", initial_prompt=prompt_to_send,language=selected_language_code)
    return result

def write_srt(file,transcription_result,file_directory="",options={}):
    if not file_directory:
        file_directory=os.path.dirname(file)
    #checking if file already exists and in case skipping it
    srt_file = os.path.splitext(file)[0] + ".srt"
    if os.path.exists(srt_file) and os.path.getsize(srt_file) > 0:
        print(f"Skipping {srt_file} because it already exists and is not empty")
        return
    writer_srt = get_writer("srt", file_directory) # get srt writer for the current directory
    writer_srt(transcription_result, file, options) # add empty dictionary for 'options'

def write_txt(file,transcription_result,file_directory="",options={}):
    if not file_directory:
        file_directory=os.path.dirname(file)
    #checking if file already exists and in case skipping it
    text_file = os.path.splitext(file)[0] + ".txt"
    if os.path.exists(text_file) and os.path.getsize(text_file) > 0:
        print(f"Skipping {text_file} because it already exists and is not empty")
        return
    writer_txt = get_writer("txt", file_directory) # get srt writer for the current directory
    writer_txt(transcription_result, file, options) # add empty dictionary for 'options'

def write_vtt(file,transcription_result,file_directory="",options={}):
    if not file_directory:
        file_directory=os.path.dirname(file)
    #checking if file already exists and in case skipping it
    vtt_file = os.path.splitext(file)[0] + ".vtt"
    if os.path.exists(vtt_file) and os.path.getsize(vtt_file) > 0:
        print(f"Skipping {vtt_file} because it already exists and is not empty")
        return
    writer_vtt = get_writer("vtt", file_directory) # get srt writer for the current directory
    writer_vtt(transcription_result, file, options) # add empty dictionary for 'options'

def write_tsv(file,transcription_result,file_directory="",options={}):
    if not file_directory:
        file_directory=os.path.dirname(file)
    #checking if file already exists and in case skipping it
    tsv_file = os.path.splitext(file)[0] + ".tsv"
    if os.path.exists(tsv_file) and os.path.getsize(tsv_file) > 0:
        print(f"Skipping {tsv_file} because it already exists and is not empty")
        return
    writer_tsv = get_writer("tsv", file_directory) # 
    writer_tsv(transcription_result, file, options) # add empty dictionary for 'options'

def write_json(file,transcription_result,file_directory="",options={}):
   

    if not file_directory:
        file_directory=os.path.dirname(file)
    #checking if file already exists and in case skipping it
    json_file = os.path.splitext(file)[0] + ".json"
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        print(f"Skipping {json_file} because it already exists and is not empty")
        return
    writer_json = get_writer("json", file_directory) # 
    writer_json(transcription_result, file, options) # not sure what are the options for json

def write_files(file,transcription_result,file_directory="",options={},selected_formats=['txt', 'srt', 'vtt', 'tsv', 'json']):
    if not file_directory:
        file_directory = os.path.dirname(file)

    if 'json' in selected_formats:
        json_options = options.get("json", {})
        write_json(file, transcription_result, file_directory, json_options)

    if 'srt' in selected_formats:
        srt_options = options.get("srt", {})
        write_srt(file, transcription_result, file_directory, srt_options)

    if 'txt' in selected_formats:
        txt_options = options.get("txt", {})
        write_txt(file, transcription_result, file_directory, txt_options)

    if 'vtt' in selected_formats:
        vtt_options = options.get("vtt", {})
        write_vtt(file,transcription_result,file_directory,vtt_options)

    if 'tsv' in selected_formats:
        tsv_options = options.get("tsv", {})
        write_tsv(file,transcription_result,file_directory,tsv_options)

# Function to list transcribable files in a directory
def list_transcribable_files(directory):
    transcribable_files = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('.'):
                continue
            # Check if the file has a transcribable extension
            if any(file.lower().endswith(ext) for ext in transcribable_extensions):
                # Add the file to the list
                transcribable_files.append(os.path.join(root, file))
    return transcribable_files


def perform_transcription(directory_to_transcribe, selected_model, options, selected_formats, prompt,selected_language_code):

    # Get the list of transcribable files
    files_to_transcribe = list_transcribable_files(directory_to_transcribe)

    # Print the list of files
    print("Files that can be transcribed:")
    for file in files_to_transcribe:
        print(file)


    for file in files_to_transcribe:
        print(f"Transcribing {file}...")
        file_directory=os.path.dirname(file)

        # the whole system of lock-unlock is being eliminated because whisper does not get better running multiple processes
        if is_file_locked(file):   unlock_file(file)

        # Check if the json file already exists and if it is old, new, or something else
        json_file = os.path.splitext(file)[0] + ".json"

        #check if the json file exists
        if os.path.exists(json_file):
            #reading the json file and placing it in the data variable
            data=json.decoder.JSONDecoder().decode(open(json_file).read())

            if is_old_json_format(data):
                text_file = os.path.splitext(file)[0] + ".txt"

                #reading the old text file
                old_text=open(text_file).read()
                old_json=data.copy()

                language=infer_language_from_text(old_text)
                new_data={}
                new_data["text"]=old_text
                new_data["segments"]=old_json
                new_data["language"]=language

                #rename json file into .old.json
                os.rename(json_file, json_file+".old")

                #write the new files
                write_files(file,new_data,file_directory,options, selected_formats)

            else:
                if is_new_json_format(data):
                    write_files(file,data,file_directory,options, selected_formats)
                else:
                    print(f"{json_file} not in the expected format, please delete it manually if you want me to continue")
                    exit(1)
        else:

            transcription_result=transcribe_file(file, selected_model,prompt,selected_language_code)
            transcribed_text =transcription_result['text']

            # Check if the transcribed text is empty
            if not transcribed_text:
                print(f"Transcribed text is empty. Skipping {file}")
                continue
            write_files(file,transcription_result,file_directory,options, selected_formats)            
        print()


def start_ui():
    def open_directory_selector():
        selected_directory = filedialog.askdirectory()  # Apre il dialogo di selezione directory
        if selected_directory:  # Se l'utente seleziona una directory
            directory_path.set(selected_directory)  # Aggiorna la variabile legata all'edit box
            directory_entry.delete(0, tk.END)  # Rimuove il testo attuale dall'edit box
            directory_entry.insert(tk.END, selected_directory)  # Inserisce il nuovo percorso nella edit box 
            transcription_button.config(state=tk.NORMAL)  # Enable the transcription button
  

    def start_transcription():
        # Logica per iniziare la trascrizione
        print("Inizio trascrizione...")

        chosen_model = selected_model.get()
        print("Selected model:", chosen_model)

        if chosen_model[-3:] == ".en":      selected_language = "english"
        else:                               selected_language = language.get()
        selected_language_code=LANGUAGES_CODES[selected_language]
        print(f"language {selected_language_code} ({selected_language}) with the model: {selected_model.get()}")

        selected_formats = [fmt for fmt, var in format_vars.items() if var.get()]
        print("selected_formats:", selected_formats)

        directory_to_check = directory_entry.get()
        print("directory_to_check:", directory_to_check)

        prompt_to_send = prompt_entry.get()
        print("prompt_to_send:", prompt_to_send)            
        # Initialize the options dictionary
        options = {}
        # Gather options for each selected format
        for fmt in selected_formats:
            # Initialize options for the current format
            format_options = {}
            
            # Get the max line width from the corresponding entry widget
            max_line_width = max_line_width_entries[fmt].get()
            # Add options to the format dictionary
            format_options["max_words_per_line"] = int(max_line_width)
            format_options["highlight_words"] = False  # Default value, can be adjusted as needed
            format_options["max_line_count"] = 1
            
            # Store the format options in the main options dictionary
            options[fmt] = format_options

        # Print the options for debugging
        print("Options:", options)
        perform_transcription(directory_to_check, chosen_model, options, selected_formats,prompt_to_send,selected_language_code)
        print("Trascrizione completata")

        
    # Inizializza l'interfaccia grafica principale
    root = tk.Tk()
    root.title("Trascrittore Whisper")

    # Directory frame
    directory_frame = tk.Frame(root)
    directory_frame.pack(pady=10)
    directory_path = tk.StringVar()
    tk.Label(directory_frame, text="Directory:").pack(side=tk.LEFT)
    directory_entry = tk.Entry(directory_frame, textvariable=directory_path, width=50)
    directory_entry.pack(side=tk.LEFT)
    tk.Button(directory_frame, text="Sfoglia", command=open_directory_selector).pack(side=tk.LEFT)

    # Model frame
    model_frame = tk.Frame(root)
    model_frame.pack(pady=10)
    selected_model = tk.StringVar(value="medium.en")

    standard_models_frame = tk.LabelFrame(model_frame, text="Standard models")
    standard_models_frame.pack(side=tk.LEFT, padx=10)
    english_models_frame = tk.LabelFrame(model_frame, text="English models")
    english_models_frame.pack(side=tk.LEFT, padx=10)

    models = [("tiny", standard_models_frame), ("small", standard_models_frame), 
              ("base", standard_models_frame), ("medium", standard_models_frame), 
              ("large", standard_models_frame), ("tiny.en", english_models_frame), 
              ("small.en", english_models_frame), ("base.en", english_models_frame), 
              ("medium.en", english_models_frame)]
    
    for model, frame in models:
        tk.Radiobutton(frame, text=model, variable=selected_model, value=model).pack(anchor=tk.W)


    # Elenco delle lingue supportate

    selected_language = tk.StringVar()


    # Menu a discesa per la selezione della lingua
    language_frame = tk.Frame(standard_models_frame)
    language_frame.pack(fill=tk.X, expand=True)
    tk.Label(language_frame, text="Language:").pack(side=tk.LEFT)
    language = tk.StringVar()
    language_combobox = ttk.Combobox(language_frame, textvariable=language, state="readonly")
    # Usa i nomi completi delle lingue come valori nel menu a discesa
    language_combobox['values'] = list(LANGUAGES.values())
    language_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
    language_combobox.set('italian')  # Imposta un valore predefinito, se necessario

    # Format frame
    format_frame = tk.LabelFrame(root, text="Output Formats")
    format_frame.pack(pady=10)
    formats = ["txt", "srt", "vtt", "tsv", "json"]
    format_vars = {fmt: tk.BooleanVar(value=True) for fmt in formats}
    max_line_width_entries = {}  # Dictionary to hold max line width entry widgets

    feedback_frame = tk.Frame(root)
    feedback_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    feedback_text = tk.Text(feedback_frame, height=10)
    feedback_text.pack(fill=tk.BOTH, expand=True)

    for fmt in formats:
        checkbox_frame = tk.Frame(format_frame)
        checkbox_frame.pack(anchor=tk.W)

        checkbox = tk.Checkbutton(checkbox_frame, text=fmt.upper(), variable=format_vars[fmt])
        checkbox.pack(side=tk.LEFT)

        max_line_width_var = tk.StringVar(value="35")  # Default max line width
        tk.Label(checkbox_frame, text="Max words per line (does not work):").pack(side=tk.LEFT)
        max_line_width_entry = tk.Entry(checkbox_frame, textvariable=max_line_width_var, width=5)
        max_line_width_entry.pack(side=tk.LEFT)
        max_line_width_entries[fmt] = max_line_width_entry  # Store entry widget in dictionary

    feedback_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    feedback_text = tk.Text(feedback_frame, height=10)
    feedback_text.pack(fill=tk.BOTH, expand=True)

    # Prompt frame
    prompt_frame = tk.Frame(root)
    prompt_frame.pack(pady=10)
    prompt_text = tk.StringVar()
    tk.Label(prompt_frame, text="Prompt:").pack(side=tk.LEFT)
    prompt_entry = tk.Entry(prompt_frame, textvariable=prompt_text, width=50)
    prompt_entry.pack(side=tk.LEFT)

    # Transcription button
    transcription_button = tk.Button(root, text="Start Transcription", command=start_transcription)
    transcription_button.pack(pady=10)
    transcription_button.config(state=tk.DISABLED)  # Disable the transcription button initially

    root.mainloop()


# Chiamata alla funzione per avviare l'interfaccia utente
start_ui()
