from ultralytics import YOLO

model = YOLO("/runs/classify/train2/weights/best.pt")

results = model("/home/andrey/PycharmProjects/neiro_training/test_dir/test_img.png")
# тут изменить путь до файла