import tkinter as tk
import threading
import socket

HOST = "127.0.0.1"  # Adresse du serveur
PORT = 5001         # Port du serveur

# Création du socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

isConnect = False

def connect():
    global isConnect
    client_socket.connect((HOST, PORT))
    label_resultat.config(text = 'Connected')
    thread = threading.Thread(target=recevoir_messages)
    thread.daemon = True
    thread.start()
    isConnect = True

def afficher_texte():
    if isConnect == True:
        nouveau = entree.get()                     # Texte saisi
        ancien = label_resultat.cget("text")       # Texte déjà affiché
        label_resultat.config(text = ancien + '\n' + nouveau)
        client_socket.send(nouveau.encode())


def recevoir_messages():
    """Écoute les messages du client sans bloquer Tkinter."""
    global client_socket
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            # Afficher le message dans le label
            label_resultat.config(text=label_resultat.cget("text") + "\nServeur : " + data)
        except:
            break

# Fenêtre principale
root = tk.Tk()
root.title("Client")

# Label pour afficher le résultat
label_resultat = tk.Label(root, text="", font=("Arial", 14))
label_resultat.pack(pady=10)

# Champ de texte
entree = tk.Entry(root, width=30)
entree.pack(pady=10)

# Bouton
bouton = tk.Button(root, text="Envoyer", command=afficher_texte)
bouton.pack(pady=5)

bouton = tk.Button(root, text="Connect me first", command=connect)
bouton.pack(pady=5)

root.mainloop()



