import glob
import os
import random
from math import floor
from tqdm import tqdm
import shutil

print('qwrqrqwrqwrq')

input_folders = [
    'datasets/flowers/daisy/',
    'datasets/flowers/dandelion/',
    'datasets/flowers/roses/',
    'datasets/flowers/sunflowers/',
    'datasets/flowers/tulips/'
]

BASE_DIR_ABSOLUTE = "C:/python/neiro_training"
OUT_DIR = 'datasets/flowers_prepared/'

OUT_TRAIN = OUT_DIR + 'train/'
OUT_VAL = OUT_DIR + 'test/'

coeff = [80, 20]
exceptions = ['classes']

if int(coeff[0]) + int(coeff[1]) > 100:
    print("Coeff can't exceed 100%.")
    exit(1)

print(f"Preparing images data by {coeff[0]}/{coeff[1]} rule.")
print(f"Source folders: {len(input_folders)}")
print("Gathering data ...")

source = {}
for sf in input_folders:
    source.setdefault(sf, [])

    os.chdir(BASE_DIR_ABSOLUTE)
    os.chdir(sf)

    for filename in glob.glob("*.jpg"):
        source[sf].append(filename)

train = {}
val = {}
for sk, sv in source.items():
    random.shuffle(sv)  # Перемешиваем данные
    split_index = floor(len(sv) * (coeff[0] / 100))  # Вычисляем индекс разделения

    train.setdefault(sk, [])
    val.setdefault(sk, [])
    train[sk] = sv[:split_index]  # Первые 80% для тренировки
    val[sk] = sv[split_index:]  # Остальные 20% для валидации

train_sum = 0
val_sum = 0

for sk, sv in train.items():
    train_sum += len(sv)

for sk, sv in val.items():
    val_sum += len(sv)

print(f"\nOverall TRAIN images count: {train_sum}")
print(f"Overall TEST images count: {val_sum}")

os.chdir(BASE_DIR_ABSOLUTE)
print("\nCopying TRAIN source items to prepared folder ...")
for sk, sv in tqdm(train.items()):
    for item in tqdm(sv):
        imgfile_source = os.path.join(BASE_DIR_ABSOLUTE, sk, item)
        imgfile_dest = os.path.join(BASE_DIR_ABSOLUTE, OUT_TRAIN, sk.split('/')[-2])

        os.makedirs(imgfile_dest, exist_ok=True)
        shutil.copyfile(imgfile_source, os.path.join(imgfile_dest, item))

os.chdir(BASE_DIR_ABSOLUTE)
print("\nCopying VAL source items to prepared folder ...")
for sk, sv in tqdm(val.items()):
    for item in tqdm(sv):
        imgfile_source = os.path.join(BASE_DIR_ABSOLUTE, sk, item)
        imgfile_dest = os.path.join(BASE_DIR_ABSOLUTE, OUT_VAL, sk.split('/')[-2])

        os.makedirs(imgfile_dest, exist_ok=True)
        shutil.copyfile(imgfile_source, os.path.join(imgfile_dest, item))
