import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Função para obter o tamanho de um ficheiro em bytes
def tamanho_ficheiro(path):
    return os.path.getsize(path)

# Função para dividir o vídeo em frames e classificar os frames
def extrair_frames_e_classificar(video_path, pasta_destino, intervalo):
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        messagebox.showerror("Erro", f"Erro ao abrir o vídeo: {video_path}")
        return

    # Obter informações do vídeo para calcular o progresso
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    total_tamanho = tamanho_ficheiro(video_path)

    frame_count = 0
    movimentos = ['anda_para_frente', 'anda_para_tras', 'vira_direita', 'vira_esquerda', 'saltar', 'abaixar_defesa']
    for movimento in movimentos:
        os.makedirs(os.path.join(pasta_destino, movimento), exist_ok=True)

    # Variável para o tamanho total dos frames extraídos
    tamanho_acumulado = 0

    # Atualizar a barra de progresso
    progress_bar["maximum"] = total_frames

    while True:
        ret, frame = video.read()

        if not ret:
            messagebox.showinfo("Fim", "Fim do vídeo.")
            break

        if frame_count % intervalo == 0:
            if frame_count % 100 == 0:
                movimento = 'anda_para_frente'
            elif frame_count % 100 == 25:
                movimento = 'anda_para_tras'
            elif frame_count % 100 == 50:
                movimento = 'vira_direita'
            elif frame_count % 100 == 75:
                movimento = 'vira_esquerda'
            elif frame_count % 300 == 0:
                movimento = 'saltar'
            else:
                movimento = 'abaixar_defesa'

            nome_frame = f"frame_{frame_count}.jpg"
            caminho_frame = os.path.join(pasta_destino, movimento, nome_frame)
            cv2.imwrite(caminho_frame, frame)

            # Atualizar o tamanho acumulado
            tamanho_acumulado += os.path.getsize(caminho_frame)

            # Atualizar a barra de progresso
            progress_bar["value"] = frame_count
            janela.update_idletasks()

            # Exibir o tamanho em GB, MB, e KB
            tamanho_gb = tamanho_acumulado / (1024 ** 3)
            tamanho_mb = tamanho_acumulado / (1024 ** 2)
            tamanho_kb = tamanho_acumulado / 1024
            tamanho_label.config(text=f"Convertido: {tamanho_gb:.2f} GB | {tamanho_mb:.2f} MB | {tamanho_kb:.2f} KB")

        frame_count += 1

    video.release()

# Funções da Interface Gráfica
def escolher_video():
    caminho_video = filedialog.askopenfilename(title="Escolher vídeo", filetypes=[("Ficheiros de vídeo", "*.mp4;*.avi")])
    if caminho_video:
        caminho_video_entry.delete(0, tk.END)
        caminho_video_entry.insert(0, caminho_video)

def escolher_pasta():
    caminho_pasta = filedialog.askdirectory(title="Escolher pasta de destino")
    if caminho_pasta:
        caminho_pasta_entry.delete(0, tk.END)
        caminho_pasta_entry.insert(0, caminho_pasta)

def iniciar_classificacao():
    video_path = caminho_video_entry.get()
    pasta_destino = caminho_pasta_entry.get()

    if not video_path or not pasta_destino:
        messagebox.showerror("Erro", "Por favor, selecione o caminho do vídeo e a pasta de destino.")
        return

    try:
        intervalo = int(intervalo_entry.get())
    except ValueError:
        messagebox.showerror("Erro", "Intervalo inválido. Insira um número.")
        return

    extrair_frames_e_classificar(video_path, pasta_destino, intervalo)

def sair():
    janela.quit()

# Criar a janela principal
janela = tk.Tk()
janela.title("Classificador de Movimentos do Avatar")

# Label e campo de texto para o caminho do vídeo
tk.Label(janela, text="Caminho do Vídeo:").grid(row=0, column=0, padx=10, pady=10)
caminho_video_entry = tk.Entry(janela, width=50)
caminho_video_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(janela, text="Escolher Vídeo", command=escolher_video).grid(row=0, column=2, padx=10, pady=10)

# Label e campo de texto para o caminho da pasta de destino
tk.Label(janela, text="Pasta de Destino:").grid(row=1, column=0, padx=10, pady=10)
caminho_pasta_entry = tk.Entry(janela, width=50)
caminho_pasta_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(janela, text="Escolher Pasta", command=escolher_pasta).grid(row=1, column=2, padx=10, pady=10)

# Label e campo de texto para o intervalo entre frames
tk.Label(janela, text="Intervalo entre Frames:").grid(row=2, column=0, padx=10, pady=10)
intervalo_entry = tk.Entry(janela, width=10)
intervalo_entry.grid(row=2, column=1, padx=10, pady=10)
intervalo_entry.insert(0, "10")  # Valor padrão para intervalo

# Barra de progresso
tk.Label(janela, text="Progresso:").grid(row=3, column=0, padx=10, pady=10)
progress_bar = ttk.Progressbar(janela, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=3, column=1, padx=10, pady=10)

# Label para exibir o tamanho em GB, MB, e KB
tamanho_label = tk.Label(janela, text="Convertido: 0 GB | 0 MB | 0 KB")
tamanho_label.grid(row=4, column=1, padx=10, pady=10)

# Botão para iniciar a classificação
tk.Button(janela, text="Iniciar Classificação", command=iniciar_classificacao).grid(row=5, column=1, padx=10, pady=10)

# Botão para sair
tk.Button(janela, text="Sair", command=sair).grid(row=6, column=1, padx=10, pady=10)

# Iniciar o loop da interface gráfica
janela.mainloop()
