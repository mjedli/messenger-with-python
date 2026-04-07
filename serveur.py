import tkinter as tk
import threading
import socket

HOST = "127.0.0.1"  # Adresse locale
PORT = 5001        # Port d'écoute


# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

client_socket = None
client_address = None

isConnect = False

def connect():
    global client_socket, client_address, isConnect
    label_resultat.config(text = 'Client not connected')
    client_socket, client_address = server_socket.accept()
    label_resultat.config(text = 'Connected')
    thread = threading.Thread(target=recevoir_messages)
    thread.daemon = True
    thread.start()
    isConnect = True


def recevoir_messages():
    """Écoute les messages du client sans bloquer Tkinter."""
    global client_socket
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            # Afficher le message dans le label
            label_resultat.config(text=label_resultat.cget("text") + "\nClient : " + data)
        except:
            break

def afficher_texte():
    if isConnect == True:
        nouveau = entree.get()                     # Texte saisi
        ancien = label_resultat.cget("text")       # Texte déjà affiché
        label_resultat.config(text = ancien + '\n' + nouveau)
        client_socket.send(nouveau.encode())


# Fenêtre principale
root = tk.Tk()
root.title("Serveur")

# Label pour afficher le résultat
label_resultat = tk.Label(root, text="", font=("Arial", 14))
label_resultat.pack(pady=10)

# Champ de texte
entree = tk.Entry(root, width=30)
entree.pack(pady=10)

# Bouton
bouton = tk.Button(root, text="Envoyer", command=afficher_texte)
bouton.pack(pady=5)

# Bouton
bouton = tk.Button(root, text="Connect me second", command=connect)
bouton.pack(pady=5)

root.mainloop()