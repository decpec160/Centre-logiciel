import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import subprocess
import os
from PIL import Image, ImageTk

class SoftwareCenterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Centre Logiciel")
        self.root.geometry("800x600")

        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect('Center.db')
        self.c = self.conn.cursor()

        # Création de la table pour stocker les applications si elle n'existe pas
        self.create_table()

        # Liste pour stocker les applications
        self.app_list = []
        self.selected_app = None

        # Mot de passe admin (à remplacer par un mécanisme sécurisé)
        self.admin_password = "admin123"

        # Création de l'interface utilisateur
        self.create_ui()

    def create_table(self):
        # Création de la table
        self.c.execute('''CREATE TABLE IF NOT EXISTS apps 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           name TEXT NOT NULL,
                           category TEXT,
                           install_cmd TEXT,
                           image_path TEXT,
                           description TEXT,
                           instructions_path TEXT)''')
        self.conn.commit()

    def create_ui(self):
        # Frame principale
        main_frame = ttk.Frame(self.root, padding=(20, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titre de l'application
        label_title = ttk.Label(main_frame, text="Centre Logiciel", font=("Helvetica", 20))
        label_title.pack(pady=10)

        # Barre de recherche
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)

        btn_search = ttk.Button(search_frame, text="Rechercher", command=self.search_apps)
        btn_search.pack(side=tk.LEFT, padx=5, pady=5)

        # Menu pour gérer les applications
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        gestion_menu = tk.Menu(menu_bar, tearoff=0)
        gestion_menu.add_command(label="Ajouter une application", command=self.open_add_app_window)
        gestion_menu.add_command(label="Supprimer l'application sélectionnée", command=self.delete_selected_app)
        menu_bar.add_cascade(label="Gérer", menu=gestion_menu)

        # Cadre pour afficher l'image et la description de l'application sélectionnée
        app_details_frame = ttk.Frame(main_frame)
        app_details_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Zone pour afficher l'image de l'application
        self.app_image_label = ttk.Label(app_details_frame)
        self.app_image_label.grid(row=0, column=0, padx=10, pady=10)

        # Zone pour afficher la description de l'application
        self.app_description = tk.Text(app_details_frame, width=40, height=6, wrap="word")
        self.app_description.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Bouton pour installer l'application sélectionnée
        btn_install_app = ttk.Button(main_frame, text="Installer l'application sélectionnée", command=self.install_selected_app)
        btn_install_app.pack(pady=10)

        # Bouton pour afficher les instructions d'installation
        btn_view_instructions = ttk.Button(main_frame, text="Voir les instructions d'installation", command=self.view_instructions)
        btn_view_instructions.pack(pady=10)

        # Liste des applications ajoutées
        self.app_listbox = tk.Listbox(main_frame, width=80, height=15)
        self.app_listbox.pack(padx=10, pady=10)
        self.app_listbox.bind('<<ListboxSelect>>', self.on_app_select)

        # Chargement initial des applications
        self.load_apps()

        # Lier la sauvegarde à la fermeture de la fenêtre principale
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def search_apps(self):
        search_term = self.search_var.get().lower()
        self.app_listbox.delete(0, tk.END)
        
        for app in self.app_list:
            if search_term in app[1].lower():  # Recherche par nom
                self.app_listbox.insert(tk.END, app[1])

    def open_add_app_window(self):
        # Vérifier l'administrateur avant d'ouvrir la fenêtre d'ajout
        if self.is_admin():
            # Fenêtre pour ajouter une application
            self.add_app_window = tk.Toplevel(self.root)
            self.add_app_window.title("Ajouter une application")
            self.add_app_window.geometry("400x500")

            # Champ pour entrer le nom de l'application
            label_name = ttk.Label(self.add_app_window, text="Nom de l'application:")
            label_name.pack(anchor='w', padx=10, pady=5)

            self.app_name_entry = ttk.Entry(self.add_app_window, width=50)
            self.app_name_entry.pack(fill='x', padx=10, pady=5)

            # Champ pour sélectionner la catégorie de l'application
            label_category = ttk.Label(self.add_app_window, text="Catégorie:")
            label_category.pack(anchor='w', padx=10, pady=5)

            self.category_var = tk.StringVar()
            self.category_var.set("OS")  # Catégorie par défaut

            self.category_menu = ttk.Combobox(self.add_app_window, textvariable=self.category_var, values=["OS", "Applications", "Jeux", "Utilitaires"], width=20)
            self.category_menu.pack(fill='x', padx=10, pady=5)

            # Champ pour afficher le chemin du fichier d'installation
            label_install_cmd = ttk.Label(self.add_app_window, text="Chemin du fichier d'installation:")
            label_install_cmd.pack(anchor='w', padx=10, pady=5)

            self.install_cmd_entry = ttk.Entry(self.add_app_window, width=50)
            self.install_cmd_entry.pack(fill='x', padx=10, pady=5)

            # Bouton pour sélectionner le fichier d'installation
            btn_browse = ttk.Button(self.add_app_window, text="Sélectionner le fichier d'installation", command=self.browse_install_file)
            btn_browse.pack(padx=10, pady=10)

            # Champ pour afficher le chemin de l'image de l'application
            label_image_path = ttk.Label(self.add_app_window, text="Chemin de l'image (optionnel):")
            label_image_path.pack(anchor='w', padx=10, pady=5)

            self.image_path_entry = ttk.Entry(self.add_app_window, width=50)
            self.image_path_entry.pack(fill='x', padx=10, pady=5)

            # Bouton pour sélectionner l'image de l'application
            btn_browse_image = ttk.Button(self.add_app_window, text="Sélectionner l'image", command=self.browse_image_file)
            btn_browse_image.pack(padx=10, pady=10)

            # Champ pour entrer la description de l'application
            label_description = ttk.Label(self.add_app_window, text="Description de l'application:")
            label_description.pack(anchor='w', padx=10, pady=5)

            self.app_description_entry = tk.Text(self.add_app_window, wrap=tk.WORD, height=4)
            self.app_description_entry.pack(fill='both', padx=10, pady=5)

            # Champ pour entrer le chemin des instructions d'installation
            label_instructions_path = ttk.Label(self.add_app_window, text="Chemin des instructions d'installation (optionnel):")
            label_instructions_path.pack(anchor='w', padx=10, pady=5)

            self.instructions_path_entry = ttk.Entry(self.add_app_window, width=50)
            self.instructions_path_entry.pack(fill='x', padx=10, pady=5)

            # Bouton pour sélectionner les instructions d'installation
            btn_browse_instructions = ttk.Button(self.add_app_window, text="Sélectionner les instructions", command=self.browse_instructions_file)
            btn_browse_instructions.pack(padx=10, pady=10)

            # Bouton pour ajouter l'application
            btn_add_app = ttk.Button(self.add_app_window, text="Ajouter l'application", command=self.add_app)
            btn_add_app.pack(fill='x', padx=10, pady=10)
        else:
            messagebox.showerror("Erreur", "Accès refusé. Mot de passe incorrect.")

    def browse_install_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.install_cmd_entry.insert(0, filepath)

    def browse_image_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.image_path_entry.insert(0, filepath)

    def browse_instructions_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.instructions_path_entry.insert(0, filepath)

    def add_app(self):
        name = self.app_name_entry.get()
        category = self.category_var.get()
        install_cmd = self.install_cmd_entry.get()
        image_path = self.image_path_entry.get()
        description = self.app_description_entry.get("1.0", tk.END).strip()
        instructions_path = self.instructions_path_entry.get()

        if name and install_cmd:
            self.c.execute("INSERT INTO apps (name, category, install_cmd, image_path, description, instructions_path) VALUES (?, ?, ?, ?, ?, ?)",
                           (name, category, install_cmd, image_path, description, instructions_path))
            self.conn.commit()
            self.load_apps()
            self.add_app_window.destroy()
        else:
            messagebox.showerror("Erreur", "Le nom et le chemin du fichier d'installation sont obligatoires.")

    def load_apps(self):
        self.app_listbox.delete(0, tk.END)
        self.app_list = self.c.execute("SELECT * FROM apps").fetchall()
        for app in self.app_list:
            self.app_listbox.insert(tk.END, app[1])

    def on_app_select(self, event):
        selected_index = self.app_listbox.curselection()
        if selected_index:
            app = self.app_list[selected_index[0]]
            self.selected_app = app
            self.display_app_details(app)

    def display_app_details(self, app):
        self.app_description.delete("1.0", tk.END)
        self.app_description.insert("1.0", app[5])

        if app[4]:
            image = Image.open(app[4])
            image = image.resize((100, 100), Image.ANTIALIAS)
            self.app_image = ImageTk.PhotoImage(image)
            self.app_image_label.config(image=self.app_image)
        else:
            self.app_image_label.config(image='')

    def install_selected_app(self):
        if self.selected_app:
            install_cmd = self.selected_app[3]
            if os.name == 'nt':
                subprocess.call(install_cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.call(install_cmd, shell=True)

    def view_instructions(self):
        if self.selected_app and self.selected_app[6]:
            try:
                with open(self.selected_app[6], "r") as file:
                    instructions = file.read()
                    messagebox.showinfo("Instructions", instructions)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire les instructions : {e}")
        else:
            messagebox.showinfo("Instructions", "Aucune instruction disponible.")

    def delete_selected_app(self):
        selected_index = self.app_listbox.curselection()
        if selected_index:
            app = self.app_list[selected_index[0]]
            confirm = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette application ?")
            if confirm:
                self.c.execute("DELETE FROM apps WHERE id = ?", (app[0],))
                self.conn.commit()
                self.load_apps()

    def is_admin(self):
        password = simpledialog.askstring("Mot de passe", "Entrez le mot de passe admin :", show='*')
        return password == self.admin_password

    def on_closing(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SoftwareCenterApp(root)
    root.mainloop()
