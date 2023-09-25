import numpy as np
import csv
import math
from criterias import criterias

#
# def read_file(filename):
#     data = []
#     with open(filename, 'r') as file:
#         reader = csv.reader(file, delimiter=';')
#         next(reader, None)  # Пропустить заголовок, если он есть
#         for row in reader:
#             data.append(
#                 criterias(float(row[0]), float(row[1]), float(row[2]), float(row[3]),
#                           float(row[4]), float(row[5]), float(row[6]), float(row[7]),
#                           float(row[8])))
#     return data
#
#
# def write_to_file():
#     print("Writing")
#
#
# def calculate_distance(data_person, search_person):
#
#     distance = 0
#     for i in range(len(data_person)):
#         distance += (data_person[i] - search_person[i]) ** 2
#     return math.sqrt(distance)
#
#
# def knn(k, data, person):
#     distances = []
#     for i in range(data):
#         distance = calculate_distance(data[i], person)
#         distances.append(person[i].coffe_or_tea, distance)
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     filename = 'data.csv'
#     filename2 = 'data.csv'
#     data = read_file(filename)
#     search_person = read_file(filename2)

import csv
import math

allergy_dict = {
    "есть": 0,
    "нету": 1
}
sex_dict = {
    "муж": 0,
    "жен": 1
}
tension_dict = {
    "пониженное": 0,
    "нормальное": 0.5,
    "повышенное": 1
}
products_dict = {
    "есть": 0,
    "нету": 1
}
health_dict = {
    "здоров": 0,
    "заболеваю": 0.5,
    "болею": 1
}

def convert_data_to_numbers(data):
    data[0] = allergy_dict[data[0]]
    data[2] = sex_dict[data[2]]
    data[3] = tension_dict[data[3]]
    data[5] = products_dict[data[5]]
    data[4] = health_dict[data[4]]
    return data

# Функция для расчета евклидова расстояния между двумя точками
def euclidean_distance(point1, point2):
    distance = 0
    for i in range(len(point1) - 1):  # Исключаем последний элемент (предпочтение)
        distance += (point1[i] - point2[i]) ** 2
    return math.sqrt(distance)

# Функция для поиска k ближайших соседей
def get_neighbors(train_data, test_instance, k):
    distances = []
    for train_instance in train_data:
        dist = euclidean_distance(train_instance, test_instance)
        distances.append((train_instance, dist))
    distances.sort(key=lambda x: x[1])
    neighbors = [item[0] for item in distances[:k]]
    return neighbors

# Функция для прогнозирования предпочтения на основе соседей
def predict_preference(neighbors):
    votes = {'чай': 0, 'кофе': 0}
    for neighbor in neighbors:
        preference = neighbor[-1]  # Последний элемент - предпочтение
        votes[preference] += 1
    predicted_preference = max(votes, key=votes.get)
    return predicted_preference

# Функция для чтения данных из CSV файла
def load_data(filename):
    dataset = []
    with open(filename, 'r', encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            row = convert_data_to_numbers(row)
            dataset.append([float(row[0]), float(row[1]), float(row[2]),
                            float(row[3]), float(row[4]), float(row[5]),
                            row[6]])
    return dataset


# Загрузка известных данных
known_data = load_data('data.csv')

# Загрузка данных без предпочтений
unknown_data = load_data('unknown.csv')

k = 3  # Задайте значение k

# Прогнозирование предпочтений для данных без предпочтений
for person in unknown_data:
    neighbors = get_neighbors(known_data, person, k)
    predicted_preference = predict_preference(neighbors)
    print(f"Предпочтение для человека: {person}, предсказание: {predicted_preference}")