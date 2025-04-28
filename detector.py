import cv2
import numpy as np
from ultralytics import YOLO
from googletrans import Translator
from deep_sort_realtime.deepsort_tracker import DeepSort
from config import BOX_COLOR, TEXT_COLOR, COUNT_TEXT_COLOR, YOLO_MODEL_PATH

class Detector:
    def __init__(self):
        # Tente usar GPU se disponível
        try:
            self.model = YOLO(YOLO_MODEL_PATH).to('cuda')
        except:
            self.model = YOLO(YOLO_MODEL_PATH)
            
        self.translator = Translator()
        # Pré-traduza classes comuns
        self.translated_names = {
            'person': 'pessoa',
            'car': 'carro',
            'bicycle': 'bicicleta',
            'dog': 'cachorro',
            'cat': 'gato',
            'chair': 'cadeira',
            'table': 'mesa',
            'book': 'livro',
            'bottle': 'garrafa',
            'laptop': 'laptop',
            'cell phone': 'celular',
            'keyboard': 'teclado',
            'mouse': 'mouse',
            'tv': 'tv',
            'cup': 'xícara'
        }
        self.tracker = DeepSort(max_age=30)

    def translate_label(self, eng_name):
        if eng_name not in self.translated_names:
            try:
                tr = self.translator.translate(eng_name, dest='pt')
                pt = tr.text if tr and hasattr(tr, 'text') else eng_name
            except Exception:
                pt = eng_name
            self.translated_names[eng_name] = pt
        return self.translated_names[eng_name]

    def detect_and_draw(self, frame, resize_factor=0.5):
        # Redimensiona o frame para processamento mais rápido
        h, w = frame.shape[:2]
        small_frame = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)
        
        # Detecção no frame redimensionado
        results = self.model(small_frame)[0]
        
        frame = np.ascontiguousarray(frame)
        counts = {}
        
        for box in results.boxes:
            # Obtém coordenadas
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Escala as coordenadas de volta para o tamanho original
            x1, y1, x2, y2 = int(x1/resize_factor), int(y1/resize_factor), int(x2/resize_factor), int(y2/resize_factor)
            
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            class_name_pt = self.translate_label(self.model.names[cls_id])

            counts[class_name_pt] = counts.get(class_name_pt, 0) + 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), BOX_COLOR, 2)
            label = f"{class_name_pt} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, TEXT_COLOR, 2)

        y = 20
        for cls, cnt in counts.items():
            text = f"{cls}: {cnt}"
            cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COUNT_TEXT_COLOR, 2)
            y += 25
        return frame