import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import openai
import csv
import asyncio
import os

"""TODO:
When successfull, open new window with the output file formated correctly.
- 1 Window with the bewertung
- 1 Window with the E-Mail
-- Separate Subject and Body
- 1 button to copy the Email to clipboard
"""


def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        return [row for row in reader]


def send_request_to_chatgpt(api_key, model, name, website, prompt):
    openai.api_key = api_key
    input_text = f"Name: {name}\nWebsite: {website}\nPrompt: {prompt}"

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"


def write_responses_to_file(output_path, responses):
    with open(output_path, mode='w', encoding='utf-8') as outfile:
        for idx, response in enumerate(responses, start=1):
            outfile.write(f"Response {idx}:\n{response}\n\n")


async def execute_script_async():
    loading_label = tk.Label(root, text="Loading...", font=("Arial", 14))
    loading_label.pack(pady=10)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
    progress_bar.pack(pady=10)
    progress_bar.start()

    root.update()

    try:
        csv_file = file_entry.get()
        output_file = output_entry.get()
        api_key = api_key_entry.get()
        model = model_entry.get()
        prompt = prompt_text.get("1.0", tk.END).strip()

        if not (csv_file and output_file and api_key and model and prompt):
            messagebox.showerror("Error", "All fields are required.")
            return

        rows = read_csv(csv_file)[:5]
        responses = []

        for row in rows:
            name = row.get("Name", "")
            website = row.get("Website", "")
            response = await send_request_to_chatgpt(api_key, model, name, website, prompt)
            responses.append(response)

        write_responses_to_file(output_file, responses)
        messagebox.showinfo("Success", f"Responses have been written to {output_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        progress_bar.stop()
        loading_label.destroy()
        progress_bar.destroy()


def execute_script():
    asyncio.run(execute_script_async())


def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def browse_output(entry):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


# Tkinter UI
root = tk.Tk()
root.title("ChatGPT Website Review App")
root.geometry("")
root.pack_propagate(1)
root.configure(padx=16, pady=16)

# Top Frame for File Inputs
top_frame = tk.Frame(root, pady=10)
top_frame.pack(fill="x")

# Input CSV File Label
file_label = tk.Label(top_frame, text="Input CSV File:")
file_label.pack(side="top", padx=5, anchor="w")

# Input CSV File Entry and Browse Button
file_entry_frame = tk.Frame(top_frame)  # Create a new frame for entry and button
file_entry_frame.pack(side="top", anchor="w")

file_entry = tk.Entry(file_entry_frame, width=70)
file_entry.pack(side="left", padx=5)  # Pack entry to the left

file_browse = tk.Button(file_entry_frame, text="Browse", command=lambda: browse_file(file_entry))
file_browse.pack(side="left", padx=5)  # Pack button to the left

# Top Frame for the Output-file input
output_frame = tk.Frame(root, pady=10)
output_frame.pack(fill="x")

#Output file Label 
output_label = tk.Label(output_frame, text="Output File:")
output_label.pack(side="top", padx=5, anchor="w")

# Output file Entry and Browse Button
output_entry_frame = tk.Frame(output_frame)
output_entry_frame.pack(side="top", anchor="w")

output_entry = tk.Entry(output_entry_frame, width=70)
output_entry.pack(side="left", padx=5)
output_browse = tk.Button(output_entry_frame, text="Browse", command=lambda: browse_output(output_entry))
output_browse.pack(side="left", padx=5)

# API Key Frame
api_key_frame = tk.Frame(root, pady=10)
api_key_frame.pack(side="top", fill="x", anchor="w")

api_key_label = tk.Label(api_key_frame, text="API Key:")
api_key_label.pack(side="top", padx=5, anchor="w")

api_key_entry = tk.Entry(api_key_frame, width=100, show="*")
api_key_entry.insert(0, os.getenv("CHATGPT_API_KEY"))
api_key_entry.pack(side="left", padx=5)

# Model Frame
model_frame = tk.Frame(root, pady=10)
model_frame.pack(fill="x")

model_label = tk.Label(model_frame, text="Model:")
model_label.pack(side="top", padx=5, anchor="w")

model_entry = tk.Entry(model_frame, width=100)
model_entry.insert(0, "gpt-4o")
model_entry.pack(side="left", padx=5)

# Prompt Frame
prompt_frame = tk.Frame(root, pady=10)
prompt_frame.pack(fill="both", expand=True)

prompt_label = tk.Label(prompt_frame, text="Prompt:")
prompt_label.pack(anchor="w", padx=5)
prompt_text = tk.Text(prompt_frame, width=70, height=15)
prompt_text.insert(tk.END, """
Bitte überprüfe die Qualität der folgenden Website und erstelle eine detaillierte Bewertung in den folgenden Kategorien. Dazu sollst du die URL notieren auf der du jeweilige Fehler gefunden hast, bzw welche Tools zum testen genutzt hast. 
Mache dazue eine Konkrete unterteilung von "Bewertung" und "E-Mail"

    Performance:
        Ladegeschwindigkeit (für Desktop und Mobile).
        Optimierung von Bildern und Medien.
        Einsatz von Caching und Komprimierung.

    Webseitenaufbau:
        Klarheit und Struktur der Navigation.
        Hierarchie der Inhalte.
        Barrierefreiheit (Accessibility).

    Design:
        Ästhetik und Professionalität.
        Farbwahl und Branding-Kohärenz.
        Lesbarkeit (Schriftarten, Größen, Kontraste).

    Responsiveness:
        Anpassungsfähigkeit auf unterschiedlichen Bildschirmgrößen (Desktop, Tablet, Smartphone).
        Funktionalität und Lesbarkeit auf mobilen Geräten.

Bewertung und Ergebnisformat:

    Nutze eine Bewertungsskala von 1 bis 10, wobei 10 exzellent ist.
    Beschreibe die Stärken und Schwächen der Website in jeder Kategorie.
    Füge konkrete Verbesserungsvorschläge hinzu, die dabei helfen könnten, die Website weiter zu optimieren.

Wichtig: Wenn du für die Bewertung zusätzliche Informationen oder Tests benötigst (z. B. Ladezeit-Analysen oder technische Details), erwähne dies explizit. Erstelle basierend auf den sichtbaren und zugänglichen Elementen der Website eine nachvollziehbare und umsetzbare Analyse.

Dein zweiter Auftrag ist folgender:

Verfasse eine E-Mail an das Geschäft, worin erklärt wird, was das hier ist, gebe mir auch die E-Mail Adresse des Geschäfts diese sollte in der csv datei stehen. 
Die E-Mail sollte folgende Punkte enthalten:

    Betreff:
        Schreibe einen passenden Betreff, der das Thema der E-Mail gut beschreibt in 5-6 Wörtern.

    Begrüssung:
        Sprich das Geschäft an, also z.B. Name des Geschäfts. 

    Einleitung:
        Stelle mich kurz vor: "Mein Name ist Lucas, ich bin Applikationsentwickler und baue nebenbei mein Portfolio aus. Beruflich designe und implementiere ich Webseiten, sei es mit WordPress, WIX oder React, sowie Animationen und Grafiken."

    Übergang:
        Erkläre, dass ich die Website des Geschäfts besucht habe und sie zwar schon gut ist, aber noch Potenzial zur Optimierung hat.

    Verbesserungsvorschläge:
        Hervorheben des Mehrwerts der Optimierung für das Geschäft.
        Führe die folgenden drei Kategorien an, die für das Geschäft wichtig sein könnten:
            Performance-Optimierung: Verbesserte Ladegeschwindigkeit und optimierte Bilder für eine bessere Nutzererfahrung und Google-Rankings.
            Barrierefreiheit und Benutzerfreundlichkeit: Anpassungen in der Navigation und Struktur, um die Seite für alle Kunden zugänglicher zu machen.
            Design-Updates: Verbesserungen in Ästhetik, Lesbarkeit und Konsistenz, um die Professionalität und den Gesamteindruck zu steigern.

    Abschluss mit Handlungsaufforderung:
        Biete meine Unterstützung an: "Gern würde ich Ihnen bei der Umsetzung dieser Optimierungen helfen, um Ihre Online-Präsenz weiter zu verbessern."
        Füge eine klare Handlungsaufforderung ein, z. B.: "Wenn Sie Interesse an einem unverbindlichen Gespräch haben, melden Sie sich gern bei mir."
        Füge einen text, wobei erwähnt wird, dass ich gerne ein Kostenloses Erstgespräch bzw ein Design prototypen anbieten kann.


    Abschluss:
        Füge Icons für die Kontaktmöglichkeiten ein sowie eine passende Formatierung.
        Kontaktmöglichkeiten:
            Email: colaco.lucasgabriel@gmail.com
            Phone: +49 78 800 95 78
            LinkedIn: https://www.linkedin.com/in/lucas-gabriel-colaco/
            Instagram: https://www.instagram.com/lucas.gabriel.cc/

Verboten:

    Keine Bewertung der Geschäftsführer oder Geschäftsführerin.
    Kein "ß" verwenden, sondern "ss" schreiben.
    Höflich, aber professionell bleiben.
    Keine generischen Begrüßungen schreiben wie z.B: "Sehr geehrte Damen und Herren".
""")
prompt_text.pack(fill="both", expand=True, padx=5, pady=5)

# Bottom Frame for Button
button_frame = tk.Frame(root, pady=10)
button_frame.pack()

run_button = tk.Button(button_frame, text="Run Script", command=execute_script, padx=20, pady=5)
run_button.pack()

# Start Tkinter loop
root.mainloop()
