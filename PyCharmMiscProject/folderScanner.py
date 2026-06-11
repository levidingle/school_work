# Import tkinter for GUI
import tkinter as tk
# Import file dialog to select folders
from tkinter import filedialog
from tkinter import ttk
import time
import os
import shutil


RED = "\033[31m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"
def fetch_folder():
    global selected_folder
    # Open folder selection dialog and store selected path
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_folder = folder_path
        folder_label.config(text=f"Selected Folder: {selected_folder}")

    else:
        folder_label.config(text="No folder selected!")


def scan_folder():
    global selected_folder

    progress["maximum"] = len(selected_folder)
    progress["value"] = 0


    # If no folder is selected, stop the function
    if not selected_folder:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "[ERROR] Please select a folder first!\n")
        return

    # Clear previous results from the text box
    result_text.delete("1.0", tk.END)



    # List of sus keywords to scan for
    sussy_words =[ # ["urgent", "password", "bank", "verify", "click", "login", "love", "sus"]
    # List of SUSSY WORDS
    # suspicious_words
        # Urgency / Pressure
        "urgent", "immediately", "asap", "action required", "important", "alert",

        # Account / Security
        "account", "account suspended", "account locked", "verify", "verification",
        "confirm", "security alert", "unauthorized", "suspicious activity",

        # Credentials
        "password", "username", "login", "signin", "credentials", "reset password",

        # Financial / Banking
        "bank", "credit card", "debit card", "payment", "transaction",
        "billing", "invoice", "refund", "transfer", "wire", "deposit",

        # Threat / Fear
        "suspended", "terminated", "blocked", "restricted", "penalty",
        "legal action", "fine", "court", "lawsuit",

        # Links / Actions
        "click here", "click below", "open link", "download", "attachment",
        "update", "upgrade", "install", "access now",

        # Personal Info Requests
        "ssn", "social security", "date of birth", "dob", "pin",
        "otp", "verification code", "security code",

        # Prize / Scam
        "winner", "won", "prize", "lottery", "free", "gift",
        "claim now", "limited offer",

        # Email Tricks
        "dear user", "dear customer", "official notice", "final warning",

        # Tech / IT Scams
        "virus detected", "malware", "system infected", "technical support",
        "remote access", "support team"
        
        # Gambling terms
        "bet", "wager", "odds", "parlay", "roulette", "blackjack"
        
        # File Types
        "powershell", "curl", "sqli", "1=1"
    ]
    # Timer
    start = time.perf_counter()

    # Counters
    files_scanned = 0
    total_matches = 0

    for filename in os.listdir(selected_folder):

        if filename.endswith(".txt"):
            file_path = os.path.join(selected_folder, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read().lower()
                found = [word for word in sussy_words if word in content]

                files_scanned += 1

                if found:
                    total_matches += 1
                    result_text.insert(tk.END, f"[WARNING] {filename}: {', '.join(found)}\n", "warning")
                else:
                    result_text.insert(tk.END, f"[SAFE] {filename}\n", "safe")

            except Exception as e:
                result_text.insert(tk.END, f"[ERROR] {filename}: {str(e)}\n")

    # Stop timer
    elapsed = time.perf_counter() - start
    # Display summary of counters

    result_text.insert(tk.END, f"\n--- Summary ---\n")
    result_text.insert(tk.END, f"Files scanned : {files_scanned}\n")
    result_text.insert(tk.END, f"Total matches : {total_matches}\n")
    result_text.insert(tk.END, f"\nScan Completed in {elapsed:.5f} seconds\n")



def save_report():
    report_content = text_widget.get(1.0, tk.END)
    file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
# def quarantine_file():
#     quarantine_content = text_widget.get(1.0, tk.END)
#

def clear_output():
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "")


# GUI Setup
root = tk.Tk()

# Set window Title
root.title("Folder Security Scanner")

# Set window size
root.geometry("800x600")

# Create title label
title = tk.Label(root, text="Scan folder for SUS text", fg="black", background="salmon", font=("Algerian", 40, "bold"))

title.pack(pady=10)

# scan_btn = tk.Button(root, text="Select and Scan Folder", command=scan_folder)
# scan_btn.pack(pady=10)

fetch_btn = tk.Button(root, text="Fetch Folder", background="yellow", command=fetch_folder)
fetch_btn.pack(pady=10)

scan_btn = tk.Button(root, text="Scan Selected Folder", background="green", command=scan_folder)
scan_btn.pack(pady=10)

clear_btn = tk.Button(root, text="Clear Output", background="red", command=clear_output)
clear_btn.pack(pady=10)

progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)
progress['value'] = 100

save_button = tk.Button(root, text="Save Report", command=save_report)
save_button.pack(pady=5)

# quarantine_button = tk.Button(root, text="Quarantine File", command=quarantine_file)
# quarantine_button.pack(pady=5)

folder_label = tk.Label(root, text="No folder selected", background='salmon', wraplength=500, fg="white")
folder_label.pack(pady=5)

#Create the text box
result_text = tk.Text(root, width=70, height=50)
result_text.pack(pady=10)

result_text.tag_config("warning", foreground="RED")
result_text.tag_config("safe", foreground="GREEN")

text_widget = tk.Text(root, height=20, width=40)
text_widget.pack(pady=5)

root.config(background="salmon")


root.mainloop()



