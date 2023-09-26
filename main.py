import csv
import math

allergy_dict = {
    "аллергия на кофе": 0,
    "аллергия на чай": 0.5,
    "нет аллергии": 1
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
    "есть чай и кофе": 0,
    "есть чай": 0.5,
    "есть кофе": 1
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
def get_distance(point1, point2):
    distance = 0
    for i in range(len(point1) - 1):
        distance += (point1[i] - point2[i]) ** 2
    return math.sqrt(distance)


# Функция для поиска k ближайших соседей
def knn(train_data, test_instance, k):
    distances = []
    for train_instance in train_data:
        dist = get_distance(train_instance, test_instance)
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
    print("Чай: " + str(votes['чай']))
    print("Кофе: " + str(votes['кофе']))
    if votes['чай'] != votes['кофе']:
        return max(votes, key=votes.get)
    else:
        print("Равные числа")
        return neighbors[0][-1]


# Функция для чтения данных из CSV файла
def load_data(filename):
    dataset = []
    with open(filename, 'r', encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            row = convert_data_to_numbers(row)                                      # Входящие данные
            dataset.append([float(row[0]), float(int(row[1]) / 100), float(row[2]), # Аллергия, возраст, пол
                            float(row[3]), float(row[4]), float(row[5]),            # Давление, самочувствие, наличие продукта
                            float(int(row[6]) / 24.0), row[7]])                     # Кол-во часов сна, предпочтение
    return dataset


known_data = load_data('data.csv')
unknown_data = load_data('unknown.csv')
k = 2

for person in unknown_data:
    neighbors = knn(known_data, person, k)
    print(neighbors)
    predicted_preference = predict_preference(neighbors)
    print(f"Предпочтение для человека: {person}, предсказание: {predicted_preference}")
