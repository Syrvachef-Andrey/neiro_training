from ultralytics import YOLO

model = YOLO("best.pt")
# тут если надо модель изменить

results = model("/home/andrey/PycharmProjects/neiro_training/test_dir/test_img.png")
# тут изменить путь до файла