import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Função para dividir o vídeo em frames e classificar os frames
def extrair_frames_e_classificar(video_path, pasta_destino, intervalo):
    """
    Extrai frames de um vídeo e classifica-os em pastas específicas.

    Parâmetros:
    - video_path: Caminho do vídeo.
    - pasta_destino: Diretório base onde as pastas de classificação serão criadas.
    - intervalo: Número de frames a serem pulados (para economizar processamento).
    """
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        messagebox.showerror("Erro", f"Erro ao abrir o vídeo: {video_path}")
        return

    frame_count = 0
    movimentos = ['anda_para_frente', 'anda_para_tras', 'vira_direita', 'vira_esquerda', 'saltar', 'abaixar_defesa']
    for movimento in movimentos:
        os.makedirs(os.path.join(pasta_destino, movimento), exist_ok=True)

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
            print(f"Frame {frame_count} classificado como '{movimento}' e salvo em {caminho_frame}")

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

# Botão para iniciar a classificação
tk.Button(janela, text="Iniciar Classificação", command=iniciar_classificacao).grid(row=3, column=1, padx=10, pady=10)

# Iniciar o loop da interface gráfica
janela.mainloop()
