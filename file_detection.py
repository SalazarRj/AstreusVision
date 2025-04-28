from utils import show_window
from detector import Detector
import cv2
import os
from tkinter import filedialog

def run_file_detection():
    detector = Detector()

    path = filedialog.askopenfilename(
        title="Selecione imagem ou vídeo",
        filetypes=[
            ("Imagens", "*.jpg *.jpeg *.png"),
            ("Vídeos", "*.mp4 *.avi *.mov"),
            ("Todos os arquivos", "*.*")
        ]
    )
    if not path:
        return

    ext = os.path.splitext(path)[1].lower()
    win_name = f"Detecção: {os.path.basename(path)}"

    if ext in ['.jpg', '.jpeg', '.png']:
        img = cv2.imread(path)
        if img is None:
            print("Erro ao abrir imagem")
            return
        show_window(win_name)
        out = detector.detect_and_draw(img, resize_factor=0.7)  # Maior resolução para imagens
        cv2.imshow(win_name, out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print("Erro ao abrir vídeo")
            return
            
        show_window(win_name)
        
        # Processa apenas alguns frames para aumentar a fluidez
        frame_count = 0
        process_every = 2  # Processa 1 a cada 3 frames
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            if frame_count % process_every == 0:
                # Processa apenas alguns frames
                frame = detector.detect_and_draw(frame, resize_factor=0.5)
            
            cv2.imshow(win_name, frame)
            if cv2.waitKey(1) == 27:
                break
                
        cap.release()
        cv2.destroyAllWindows()