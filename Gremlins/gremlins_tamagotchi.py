import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time

# ----------------------------
#  Classe Tamagotchi
# ----------------------------
class Tamagotchi:
    def __init__(self):
        self.vida = 100
        self.energia = 100
        self.fome = 0
        self.estado = "normal"

        # Inicia o processo de diminuição de energia ao longo do tempo
        threading.Thread(target=self.decair_atributos, daemon=True).start()

    def decair_atributos(self):
        while True:
            time.sleep(2)
            self.energia -= 2
            self.fome += 2
            self.vida -= 1

            if self.energia <= 0 or self.fome >= 100:
                self.vida -= 5

            atualizar_interface()

    def dormir(self):
        self.estado = "dormindo"
        self.energia = min(100, self.energia + 30)
        atualizar_interface()

    def comer(self):
        self.estado = "comendo"
        self.fome = max(0, self.fome - 40)
        atualizar_interface()

    def beber(self):
        self.estado = "bebendo"
        self.fome = max(0, self.fome - 20)
        self.energia = min(100, self.energia + 10)
        atualizar_interface()

# ----------------------------
#  Interface Tkinter
# ----------------------------
tmg = Tamagotchi()

root = tk.Tk()
root.title("Meu Tamagotchi")
root.geometry("420x520")
root.resizable(False, False)

# ----------------------------
# Carregar imagens
# ----------------------------
img_normal = ImageTk.PhotoImage(Image.open("dormindo.jpg").resize((350,300)))
img_dormir = ImageTk.PhotoImage(Image.open("dormindo.jpg").resize((350,300)))
img_comer = ImageTk.PhotoImage(Image.open("comer.jpg").resize((350,300)))
img_beber = ImageTk.PhotoImage(Image.open("beber.jpg").resize((350,300)))

# ----------------------------
# Elementos da tela
# ----------------------------
label_imagem = tk.Label(root, image=img_normal)
label_imagem.pack(pady=10)

label_status = tk.Label(root, text="", font=("Arial", 14))
label_status.pack()

# Botões
frame = tk.Frame(root)
frame.pack(pady=20)

btn_dormir = tk.Button(frame, text="Dormir", width=10, command=tmg.dormir)
btn_dormir.grid(row=0, column=0, padx=5)

btn_comer = tk.Button(frame, text="Comer", width=10, command=tmg.comer)
btn_comer.grid(row=0, column=1, padx=5)

btn_beber = tk.Button(frame, text="Beber", width=10, command=tmg.beber)
btn_beber.grid(row=0, column=2, padx=5)

# ----------------------------
# Atualizar interface
# ----------------------------
def atualizar_interface():
    if tmg.estado == "normal":
        label_imagem.config(image=img_normal)
    elif tmg.estado == "dormindo":
        label_imagem.config(image=img_dormir)
    elif tmg.estado == "comendo":
        label_imagem.config(image=img_comer)
    elif tmg.estado == "bebendo":
        label_imagem.config(image=img_beber)

    label_status.config(
        text=f"Vida: {tmg.vida}\nEnergia: {tmg.energia}\nFome: {tmg.fome}"
    )

    if tmg.vida <= 0:
        messagebox.showerror("Game Over", "Seu Tamagotchi não resistiu!")
        root.destroy()

# Atualização constante da UI
def loop_interface():
    atualizar_interface()
    root.after(500, loop_interface)

loop_interface()
root.mainloop()
