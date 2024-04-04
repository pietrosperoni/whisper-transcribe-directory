import os
import markdown
import tkinter as tk
from tkinter import filedialog, ttk



def choose_directory():
    # Initialize the Tkinter root element
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # Open a dialog window for choosing a directory
    directory_path = filedialog.askdirectory(initialdir=desktop_path)
    return directory_path


def merge_text_files(directory):
    """
    Unisce tutti i file .txt in un unico file .md nella directory specificata.

    Args:
        directory (str): Percorso alla directory da analizzare.
    """

    # Crea un file markdown vuoto
    with open(os.path.join(directory, "unione.md"), "w") as f:
        f.write("")

    # Per ogni file nella directory
    for file in os.listdir(directory):
        # Se è un file .txt
        if file.endswith(".txt") or file.endswith(".md"):
        # Leggi il contenuto del file
            with open(os.path.join(directory, file), "r") as f:
                contenuto_file = f.read()

        # Crea un titolo markdown con il nome del file
            if file.endswith(".txt"):     titolo_md = f"## {file[:-4]}"
            else:                         titolo_md = f"## {file[:-3]}"

            # Aggiungi il titolo e il contenuto del file al file markdown
            with open(os.path.join(directory, f"{directory}.md"), "a") as f:
                f.write(titolo_md + "\n\n" + contenuto_file + "\n\n")

    # Controlla se ci sono sottodirectory
    for subdir in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, subdir)):
        # Ricorsivamente unisci i file nella sottodirectory
            merge_text_files(os.path.join(directory, subdir))

# Esegui la funzione nella directory specificata
      

merge_text_files(choose_directory())
