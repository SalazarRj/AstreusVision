# screen_monitor.py
import cv2
import time
import threading
from mss import mss
import numpy as np
from utils import show_window
from detector import Detector

# Configurações
MONITOR_CONFIG = {"top": 0, "left": 0, "width": 1280, "height": 720}
FPS = 120  # FPS de exibição
DETECT_INTERVAL = 0.10  # segundos entre detecções

# Variáveis globais para comunicação entre threads
detections = []  # lista de detecções atuais (x1, y1, x2, y2, label, conf)
detections_lock = threading.Lock()

def detection_worker(detector, stop_event):
    """Thread que captura frames para detecção em intervalos e atualiza `detections`."""
    with mss() as sct:
        monitor = sct.monitors[1]
        while not stop_event.is_set():
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)[..., :3]
            frame = np.ascontiguousarray(frame)

            # Roda detecção com YOLO
            results = detector.model(frame)[0]
            new_dets = []
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                label = detector.translate_label(detector.model.names[cls_id])
                conf = float(box.conf[0])
                new_dets.append((x1, y1, x2, y2, label, conf))

            # Atualiza detecções de forma segura
            with detections_lock:
                detections.clear()
                detections.extend(new_dets)

            time.sleep(DETECT_INTERVAL)

def run_screen_monitor():
    detector = Detector()
    show_window("Monitor Detecção")
    stop_event = threading.Event()

    # Inicia thread de detecção
    thread = threading.Thread(target=detection_worker, args=(detector, stop_event))
    thread.daemon = True
    thread.start()

    print("Monitor: ESC para voltar")
    prev_time = 0
    frame_time = 1 / FPS

    with mss() as sct:
        monitor = MONITOR_CONFIG
        while True:
            current_time = time.time()
            if (current_time - prev_time) >= frame_time:
                prev_time = current_time

                sct_img = sct.grab(monitor)
                frame = np.array(sct_img)[..., :3]
                frame = np.ascontiguousarray(frame)

                # Desenha informações
                with detections_lock:
                    # Contagem de objetos
                    counter = {}
                    for detection in detections:
                        label = detection[4]
                        counter[label] = counter.get(label, 0) + 1

                    # Exibe contagem no canto superior esquerdo
                    y_offset = 30
                    for label, count in counter.items():
                        text = f"{label}: {count}"
                        cv2.putText(frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
                        y_offset += 30

                    # Desenha caixas e confiança
                    for (x1, y1, x2, y2, label, conf) in detections:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                        text = f"{label} {conf:.2f}"
                        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

                cv2.imshow("Monitor Detecção", frame)

            if cv2.waitKey(1) == 27:  # ESC
                break

    # Para a thread e fecha
    stop_event.set()
    thread.join()
    cv2.destroyAllWindows()