from ultralytics import YOLO

# 1) Carrega modelo YOLOv8 nano pré-treinado em COCO
model = YOLO("yolov8x.pt")

# 2) Realiza inferência em uma imagem local
results = model("caminho/para/sua_imagem.jpg")

# 3) Exibe a imagem com bounding boxes e rótulos
results.show()
