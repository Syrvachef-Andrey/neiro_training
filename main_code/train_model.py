from ultralytics import YOLO

model = YOLO('yolo11n-cls.pt')

results = model.train(data="/home/andrey/PycharmProjects/neiro_training/datasets/flowers_prepared", epochs=50, imgsz=200)
