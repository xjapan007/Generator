import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import random
import string
import threading
from openpyxl import Workbook

class ComboGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Générateur de Combos RGB Pro")
        self.root.geometry("800x700")
        self.root.configure(bg="#1e1e1e")

        # Variables
        self.user_length_var = tk.IntVar(value=8)
        self.pass_length_var = tk.IntVar(value=8)
        self.combo_type_var = tk.StringVar(value="alphanum")
        self.fixed_user_var = tk.StringVar()
        self.fixed_pass_var = tk.StringVar()
        self.fix_var = tk.StringVar(value="aucun")
        self.prefix_var = tk.StringVar()
        self.suffix_var = tk.StringVar()
        self.include_special_var = tk.BooleanVar(value=False)
        self.num_combos_var = tk.IntVar(value=1000)
        self.rainbow_enabled = False
        self.text_color = "white"
        self.button_color = "#3c3f41"
        self.entry_color = "#3c3f41"
        self.bg_color = "#1e1e1e"
        self.label_color = "white"
        self.user_color = "#ff8c00"
        self.pass_color = "#00d4ff"
        self.text_bg_color = "#2d2d2d"
        self.progress = 0
        self.progress_max = 100
        self.stop_generation = False

        # Interface
        self.setup_ui()

    def setup_ui(self):
        # Style sombre personnalisé
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.label_color, font=("Helvetica", 10))
        self.style.configure("TButton", background=self.button_color, foreground=self.text_color, font=("Helvetica", 10))
        self.style.configure("TEntry", fieldbackground=self.entry_color, foreground=self.text_color)
        self.style.configure("TCombobox", fieldbackground=self.entry_color, foreground=self.text_color)
        self.style.configure("TNotebook.Tab", background=self.bg_color, foreground=self.label_color, font=("Helvetica", 10))
        self.style.map("TButton", background=[("active", "#4a4d4f")], foreground=[("active", self.text_color)])
        self.style.configure("Horizontal.TProgressbar", background="#00d4ff", thickness=20)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Onglets
        tab_control = ttk.Notebook(main_frame)
        tab_generate = ttk.Frame(tab_control)
        tab_settings = ttk.Frame(tab_control)
        tab_control.add(tab_generate, text="Générateur")
        tab_control.add(tab_settings, text="Paramètres")
        tab_control.pack(expand=1, fill="both")

        # Onglet Générateur
        ttk.Label(tab_generate, text="Longueur User:").grid(row=0, column=0, sticky=tk.W, pady=5)
        user_length_frame = ttk.Frame(tab_generate)
        user_length_frame.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Scale(user_length_frame, from_=4, to=25, variable=self.user_length_var, orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(user_length_frame, textvariable=self.user_length_var, width=3).pack(side=tk.LEFT, padx=5)

        ttk.Label(tab_generate, text="Longueur Pass:").grid(row=1, column=0, sticky=tk.W, pady=5)
        pass_length_frame = ttk.Frame(tab_generate)
        pass_length_frame.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Scale(pass_length_frame, from_=4, to=25, variable=self.pass_length_var, orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(pass_length_frame, textvariable=self.pass_length_var, width=3).pack(side=tk.LEFT, padx=5)

        ttk.Label(tab_generate, text="Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Combobox(tab_generate, textvariable=self.combo_type_var, values=["numérique", "alphabétique", "alphanumérique"], state="readonly").grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(tab_generate, text="Fixer:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Combobox(tab_generate, textvariable=self.fix_var, values=["aucun", "user", "pass"], state="readonly").grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(tab_generate, text="Valeur fixe:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.fixed_entry = ttk.Entry(tab_generate, textvariable=self.fixed_user_var)
        self.fixed_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(tab_generate, text="Préfixe:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(tab_generate, textvariable=self.prefix_var).grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(tab_generate, text="Suffixe:").grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Entry(tab_generate, textvariable=self.suffix_var).grid(row=6, column=1, sticky=tk.EW, padx=5, pady=5)

        tk.Checkbutton(tab_generate, text="Inclure caractères spéciaux", variable=self.include_special_var, fg=self.label_color, bg=self.bg_color, selectcolor=self.bg_color).grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        ttk.Label(tab_generate, text="Nombre de combos:").grid(row=8, column=0, sticky=tk.W, pady=5)
        ttk.Entry(tab_generate, textvariable=self.num_combos_var).grid(row=8, column=1, sticky=tk.EW, padx=5, pady=5)

        # Boutons de génération
        button_frame = ttk.Frame(tab_generate)
        button_frame.grid(row=9, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Générer", command=self.start_generation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Arrêter", command=self.stop_generation_thread).pack(side=tk.LEFT, padx=5)

        # Barre de progression
        self.progress_bar = ttk.Progressbar(tab_generate, orient=tk.HORIZONTAL, length=400, mode='determinate', style="Horizontal.TProgressbar")
        self.progress_bar.grid(row=10, column=0, columnspan=2, pady=10, padx=5, sticky=tk.EW)
        self.progress_label = ttk.Label(tab_generate, text="0%", foreground=self.label_color, background=self.bg_color)
        self.progress_label.grid(row=10, column=2, pady=10, padx=5, sticky=tk.W)

        # Zone de résultat avec tags pour les couleurs
        self.result_text = tk.Text(tab_generate, height=15, wrap=tk.WORD, bg=self.text_bg_color, fg=self.text_color, font=("Courier", 10))
        self.result_text.grid(row=11, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        self.result_text.tag_config("user", foreground=self.user_color)
        self.result_text.tag_config("pass", foreground=self.pass_color)

        # Boutons de sauvegarde
        save_frame = ttk.Frame(tab_generate)
        save_frame.grid(row=12, column=0, columnspan=2, pady=5)
        ttk.Button(save_frame, text="Sauvegarder en TXT", command=lambda: self.export_combos("txt")).pack(side=tk.LEFT, padx=5)
        ttk.Button(save_frame, text="Sauvegarder en Excel", command=lambda: self.export_combos("xlsx")).pack(side=tk.LEFT, padx=5)

        # Onglet Paramètres
        ttk.Label(tab_settings, text="Couleur Texte:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Button(tab_settings, text="Choisir", command=self.choose_text_color).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(tab_settings, text="Couleur User:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Button(tab_settings, text="Choisir", command=self.choose_user_color).grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(tab_settings, text="Couleur Pass:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Button(tab_settings, text="Choisir", command=self.choose_pass_color).grid(row=2, column=1, sticky=tk.W, pady=5)

        # Bind pour changer l'entrée fixe
        self.fix_var.trace_add("write", self.update_fixed_entry)

    def update_fixed_entry(self, *args):
        if self.fix_var.get() == "user":
            self.fixed_entry.config(textvariable=self.fixed_user_var)
        elif self.fix_var.get() == "pass":
            self.fixed_entry.config(textvariable=self.fixed_pass_var)
        else:
            self.fixed_entry.config(textvariable=tk.StringVar(value=""))

    def choose_text_color(self):
        color = colorchooser.askcolor(title="Choisir couleur Texte")[1]
        if color:
            self.text_color = color
            self.style.configure("TLabel", foreground=color)
            self.style.configure("TButton", foreground=color)
            self.style.configure("TEntry", foreground=color)
            self.result_text.config(fg=color)

    def choose_user_color(self):
        color = colorchooser.askcolor(title="Choisir couleur User")[1]
        if color:
            self.user_color = color
            self.result_text.tag_config("user", foreground=color)

    def choose_pass_color(self):
        color = colorchooser.askcolor(title="Choisir couleur Pass")[1]
        if color:
            self.pass_color = color
            self.result_text.tag_config("pass", foreground=color)

    def start_generation(self):
        self.stop_generation = False
        self.result_text.delete(1.0, tk.END)
        self.progress_bar["value"] = 0
        self.progress_label["text"] = "0%"

        num_combos = self.num_combos_var.get()
        self.progress_max = num_combos

        thread = threading.Thread(target=self.generate_combos, args=(num_combos,))
        thread.daemon = True
        thread.start()

        self.root.after(100, self.update_progress)

    def stop_generation_thread(self):
        self.stop_generation = True

    def generate_combos(self, num_combos):
        user_length = self.user_length_var.get()
        pass_length = self.pass_length_var.get()
        combo_type = self.combo_type_var.get()
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        include_special = self.include_special_var.get()
        fix_type = self.fix_var.get()
        fixed_value = self.fixed_user_var.get() if fix_type == "user" else self.fixed_pass_var.get()

        chars = ""
        if combo_type == "numérique":
            chars = string.digits
        elif combo_type == "alphabétique":
            chars = string.ascii_letters
        elif combo_type == "alphanumérique":
            chars = string.ascii_letters + string.digits
        if include_special:
            chars += string.punctuation

        combos = []
        for i in range(num_combos):
            if self.stop_generation:
                break
            if fix_type == "user":
                user = fixed_value
                passwd = ''.join(random.choice(chars) for _ in range(pass_length))
            elif fix_type == "pass":
                user = ''.join(random.choice(chars) for _ in range(user_length))
                passwd = fixed_value
            else:
                user = ''.join(random.choice(chars) for _ in range(user_length))
                passwd = ''.join(random.choice(chars) for _ in range(pass_length))
            combos.append(f"{prefix}{user}:{passwd}{suffix}")
            self.progress = i + 1

        if not self.stop_generation:
            self.root.after(0, self.display_combos, combos, prefix)

        self.progress = num_combos
        self.root.after(0, lambda: messagebox.showinfo("Info", f"Génération terminée! {len(combos)} combos générés."))

    def display_combos(self, combos, prefix):
        self.result_text.insert(tk.END, "\n".join(combos) + "\n")
        start_line = float(self.result_text.index(tk.END)) - len(combos) - 1
        for combo in combos:
            start = f"{int(start_line)}.0"
            end = f"{int(start_line)}.{len(combo)}"
            user_end = f"{start}+{len(prefix)+len(combo.split(':')[0])}c"
            self.result_text.tag_add("user", start, user_end)
            self.result_text.tag_add("pass", user_end, end)
            start_line += 1

    def update_progress(self):
        self.progress_bar["value"] = (self.progress / self.progress_max) * 100
        self.progress_label["text"] = f"{int((self.progress / self.progress_max) * 100)}%"
        if self.progress < self.progress_max and not self.stop_generation:
            self.root.after(100, self.update_progress)

    def export_combos(self, file_type):
        combos = self.result_text.get(1.0, tk.END).strip()
        if not combos:
            messagebox.showwarning("Avertissement", "Aucun combo à exporter.")
            return

        if file_type == "txt":
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
            if file_path:
                with open(file_path, "w") as f:
                    f.write(combos)
                messagebox.showinfo("Succès", "Combos sauvegardés en TXT.")
        elif file_type == "xlsx":
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Fichiers Excel", "*.xlsx")])
            if file_path:
                wb = Workbook()
                ws = wb.active
                for i, combo in enumerate(combos.split("\n"), start=1):
                    ws[f"A{i}"] = combo
                wb.save(file_path)
                messagebox.showinfo("Succès", "Combos sauvegardés en Excel.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ComboGeneratorApp(root)
    root.mainloop()
