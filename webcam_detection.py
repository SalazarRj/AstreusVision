import cv2
import time
import threading
from utils import show_window
from detector import Detector

class WebcamStream:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise ValueError("Não foi possível abrir webcam")
        
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Definir resolução menor pode melhorar o desempenho
        target_width = 640  # Você pode ajustar conforme necessário
        target_height = 480  # Você pode ajustar conforme necessário
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_height)
        
        # Atualiza os valores depois de definir
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.grabbed, self.frame = self.cap.read()
        self.stopped = False
        self.lock = threading.Lock()
        self.fps = 0

    def start(self):
        threading.Thread(target=self.update, daemon=True).start()
        return self

    def update(self):
        last_time = time.time()
        frames = 0
        
        while not self.stopped:
            if not self.cap.isOpened():
                self.stopped = True
                break
                
            grabbed, frame = self.cap.read()
            
            if not grabbed:
                self.stopped = True
                break
                
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame
                
            # Calcula FPS do stream
            frames += 1
            now = time.time()
            if now - last_time > 1.0:
                self.fps = frames / (now - last_time)
                frames = 0
                last_time = now
                
            # Pequena pausa para evitar sobrecarga da CPU
            time.sleep(0.001)

    def read(self):
        with self.lock:
            return self.grabbed, self.frame.copy() if self.grabbed else None, self.fps

    def stop(self):
        self.stopped = True
        if self.cap.isOpened():
            self.cap.release()

def run_webcam():
    detector = Detector()
    
    try:
        webcam = WebcamStream(src=0).start()
    except ValueError as e:
        print(e)
        return

    print("Webcam: ESC para voltar")
    show_window("Webcam Detecção")
    
    cv2.namedWindow("Webcam Detecção", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Webcam Detecção", webcam.frame_width, webcam.frame_height)

    frame_count = 0
    skip_frames = 2  # Processa a cada X frames
    
    last_processed_frame = None
    
    while True:
        grabbed, frame, cam_fps = webcam.read()
        if not grabbed or frame is None:
            break

        frame_count += 1
        
        # Exibe o FPS da câmera
        cv2.putText(frame, f"Cam FPS: {int(cam_fps)}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if frame_count % skip_frames == 0:
            # Frame que será processado
            start_time = time.time()
            processed_frame = detector.detect_and_draw(frame, resize_factor=0.5)
            process_time = time.time() - start_time
            
            # Exibe informações de processamento
            cv2.putText(processed_frame, f"Tempo: {process_time:.3f}s", (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            last_processed_frame = processed_frame
        
        # Exibe o último frame processado ou o frame atual sem processamento
        display_frame = last_processed_frame if last_processed_frame is not None else frame
        
        cv2.imshow("Webcam Detecção", display_frame)
        
        if cv2.waitKey(1) == 27:  # ESC
            break

    webcam.stop()
    cv2.destroyAllWindows()