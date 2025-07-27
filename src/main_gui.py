import tkinter as tk
from tkinter import messagebox
from zxcvbn import zxcvbn
import itertools
import os

# ----------------------- WORDLIST LOGIC ----------------------- #
def leetify(word):
    leet_replacements = {
        'a': ['a', '@', '4'],
        'e': ['e', '3'],
        'i': ['i', '1', '!'],
        'o': ['o', '0'],
        's': ['s', '$', '5']
    }
    patterns = [[c] if c not in leet_replacements else leet_replacements[c] for c in word.lower()]
    return [''.join(p) for p in itertools.product(*patterns)]

def generate_wordlist(inputs):
    wordlist = set()
    for base in inputs:
        leet_versions = leetify(base)
        for word in leet_versions:
            wordlist.add(word)
            wordlist.add(word + "123")
            wordlist.add(word + "2025")
            wordlist.add(word.capitalize())
            wordlist.add(word[::-1])  # reversed

    with open("wordlist.txt", "w") as f:
        for word in sorted(wordlist):
            f.write(word + "\n")
    return len(wordlist)

# ------------------------ GUI LOGIC ------------------------ #
def analyze_password():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("Warning", "Please enter a password.")
        return

    result = zxcvbn(password)
    score_label.config(text=f"Score: {result['score']}/4")
    time_label.config(text=f"Crack Time: {result['crack_times_display']['offline_fast_hashing_1e10_per_second']}")
    warning_label.config(text=f"Warning: {result['feedback']['warning'] or 'None'}")
    suggestions = result['feedback']['suggestions']
    suggestion_label.config(text=f"Suggestions: {', '.join(suggestions) if suggestions else 'None'}")

def generate():
    raw = custom_inputs_entry.get()
    if not raw:
        messagebox.showwarning("Warning", "Please enter some inputs (name, date, etc.)")
        return

    inputs = [item.strip() for item in raw.split(',') if item.strip()]
    total = generate_wordlist(inputs)
    messagebox.showinfo("Done", f"Wordlist generated with {total} entries.\nSaved as 'wordlist.txt'.")

# ------------------------ TKINTER GUI ------------------------ #
root = tk.Tk()
root.title("Password Strength Analyzer + Wordlist Generator")
root.geometry("500x400")
root.resizable(False, False)

# Styling (minimal)
tk.Label(root, text="Password Strength Analyzer", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Enter Password:").pack()
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)

tk.Button(root, text="Analyze", command=analyze_password).pack(pady=5)

score_label = tk.Label(root, text="Score: ")
score_label.pack()
time_label = tk.Label(root, text="Crack Time: ")
time_label.pack()
warning_label = tk.Label(root, text="Warning: ")
warning_label.pack()
suggestion_label = tk.Label(root, text="Suggestions: ")
suggestion_label.pack()

tk.Label(root, text="\nGenerate Wordlist from Personal Inputs", font=("Arial", 12)).pack(pady=10)
tk.Label(root, text="Enter inputs (comma-separated):").pack()
custom_inputs_entry = tk.Entry(root, width=40)
custom_inputs_entry.pack(pady=5)

tk.Button(root, text="Generate Wordlist", command=generate).pack(pady=5)

tk.Label(root, text="By Khan", font=("Arial", 9, "italic")).pack(side="bottom", pady=10)

root.mainloop()
