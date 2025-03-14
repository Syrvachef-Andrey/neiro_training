import matplotlib.pyplot as plt
from time import time
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from torch.autograd import Variable
from progress.bar import IncrementalBar
import pandas as pd

from model.test.main_test import NeuralNetwork

# Создаем собственный класс Dataset
class CustomDataset(Dataset):
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs[idx], self.labels[idx]

# Определяем устройство (GPU или CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

epochs = 500

if __name__ == "__main__":
    dataset_xlsx = pd.ExcelFile("/home/andrey/PycharmProjects/oil_repository/data_directory/data.xlsx")
    dataset_raw = dataset_xlsx.parse("Лист1")

    # Перенос модели на GPU
    model = NeuralNetwork().to(device)

    optimizer = torch.optim.SGD(model.parameters(), lr=0.04, weight_decay=0.001)

    inputs = torch.tensor(dataset_raw.values[:, 0:4].astype(np.float32))  # Используем float32
    labels = torch.tensor(dataset_raw.values[:, 4:5].astype(np.float32))  # Используем float32

    # Нормализация данных
    inputs_min = inputs.min(dim=0, keepdim=True).values
    inputs_max = inputs.max(dim=0, keepdim=True).values
    inputs = (inputs - inputs_min) / (inputs_max - inputs_min)

    labels_min = labels.min(dim=0, keepdim=True).values
    labels_max = labels.max(dim=0, keepdim=True).values
    labels = (labels - labels_min) / (labels_max - labels_min)

    # Создаем Dataset и DataLoader
    dataset = CustomDataset(inputs, labels)
    data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

    loss = 0

    st = time()
    print(f"Count epoch = {epochs}")
    bar = IncrementalBar('Model train...', max=epochs)

    for epoch in range(epochs):
        for batch_inputs, batch_labels in data_loader:
            # Перенос данных на GPU
            batch_inputs = Variable(batch_inputs).to(device)
            batch_labels = Variable(batch_labels).to(device)

            # Прямое распространение
            outputs = model(batch_inputs)

            # Обратное распространение и оптимизация
            loss = torch.nn.functional.l1_loss(outputs, batch_labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        loss = loss.item()

        print(f"Epochs {epoch}, loss {loss}")

    bar.finish()

    print(f"Loss = {loss}")
    print(f"Trained time = {round(time() - st, 2)} секунд")

    # Сохранение модели
    torch.save(model.state_dict(), "/home/andrey/PycharmProjects/oil_repository/trained_data/test/model.pt")

    # Визуализация и сохранение графика
    model.eval()
    with torch.no_grad():
        # Перенос входных данных на GPU для предсказания
        inputs = inputs.to(device)
        predictions = model(inputs).cpu().numpy()  # Возвращаем данные на CPU для визуализации

    labels_min = labels_min.numpy()
    labels_max = labels_max.numpy()

    # Возвращаем данные к исходному масштабу
    predictions = predictions * (labels_max - labels_min) + labels_min
    labels_original = labels.numpy() * (labels_max - labels_min) + labels_min

    with open("/home/andrey/PycharmProjects/oil_repository/trained_data/test/predicted_data.txt", "w", encoding="utf-8") as file:
        print("Предсказанные значения | Реальные значения")
        print("-----------------------------------------")
        file.write("Предсказанные значения | Реальные значения\n")
        file.write("------------------------------------------\n")
        for i in range(200):
            print(f"{predictions[i][0]:<20} | {labels_original[i][0]}")
            file.write(f"{predictions[i][0]:<20} | {labels_original[i][0]}\n")

    # Расчет средней квадратичной ошибки (MSE)
    mse_sqrt = np.sqrt(np.mean((predictions - labels_original) ** 2))
    print(f"Корень средней квадратичной ошибка (MSE): {mse_sqrt}")

    mae = np.mean(np.abs(predictions - labels_original))
    print(f"Средняя абсолютная ошибка (MAE): {mae}")

    plt.figure(figsize=(10, 6))
    plt.title(label=f"Корень квадратичной ошибки = {mse_sqrt}, абсолютная ошибка = {mae}", loc="center")
    plt.plot(labels_original, label='Реальные значения (labels)', color='blue')
    plt.plot(predictions, label='Предсказанные значения', color='orange', linestyle='--')
    plt.xlabel('Примеры')
    plt.ylabel('Значения')
    plt.legend()
    plt.grid(True)

    # Сохранение графика
    plt.savefig("/home/andrey/PycharmProjects/oil_repository/trained_data/test/graph.png")
    plt.show()