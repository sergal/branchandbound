import argparse

# Класс, представляющий путь по графу
class Path:

    def __init__(self, length, route_tail):
        """
        Конструктор
        :param length: длина пути
        :param route_tail: список хвостовых вершин пути

        """
        self.__length = length
        self.__route = route_tail

    @property
    def length(self):
        # Свойство, возвращающее длину пути
        return self.__length

    @property
    def route_str(self):
        """
        Свойство, возвращающее строковое представление пути
        В элементах берется e+1, так как вершины считаются от нуля, а в человеческом представлении удобно считать с единицы

        """
        return " -> ".join([str(e+1) for e in self.__route])

    def add_route_head(self, elem):
        """
        Добавить элемент к голове пути
        :param elem: элемент для добавления
        :return: измененный список-маршрут

        """
        self.__route = [elem] + self.__route


matrix = list()


def is_matrix_correct(size):
    # Функция проверки матрицы на корректность
    return all({len(line) == size for line in matrix})


def step(from_point, first_point, curr_sum, min_sum, tail):
    """
    Основная рекурсивная функция
    :param from_point: точка маршрута, в которой мы находимся в данный момент
    :param first_point: начальная точка маршрута
    :param curr_sum: текущая "стоимость" маршрута
    :param min_sum: минимальная известная "стоимость" полного маршрута. None если ещё не подсчитана
    :param tail: непройденные вершины маршрута
    :return: объект Path с минимально известной стоимостью и маршутом после прохождения данной точки рекурсии
             None если получившийся маршрут не минимален

    """
    if min_sum is not None and curr_sum > min_sum:
        return None

    if len(tail) == 0:
        curr_sum += matrix[from_point][first_point]
        return Path(curr_sum, [from_point, first_point]) if (min_sum is None or curr_sum < min_sum) else None

    new_min = min_sum
    path = None
    for elem in tail:
        result = step(elem, first_point, curr_sum + matrix[from_point][elem], new_min, tail.difference({elem}))
        if result is not None:
            new_min = result.length
            path = result
            path.add_route_head(from_point)
    return path


def min_path(start_point, size):
    """
    Функция подсчета минимального пути
    :param start_point: начальная точка пути
    :param size: размер матрицы
    :return: объект Path с минимальной стоимостью и маршутом

    """
    return step(start_point, start_point, 0, None, set(range(0, size)).difference({start_point}))

# считываем аргументы командной строки
parser = argparse.ArgumentParser(description='Программа нахождения минимального по стоимости гамильтонова цикла '
                                            + 'во взвешеном ориентированном полном графе методом ветвей и границ')

parser.add_argument('-f', '--file', default='matrix.txt', help='Файл с матрицей')
parser.add_argument('-s', '--start', default=None, type=int, help='Номер стартовой вершины')

args = parser.parse_args()
filename = args.file
start_point = args.start

# cчитываем файл
try:
    with open(filename) as f:
        for line in f:
            matrix.append([int(elem) for elem in line.split()])

except FileNotFoundError:
    print(str.format("Не найден файл {}. Положите его в ту же папку, что и этот скрипт", filename))
    exit()

size = len(matrix)

if not is_matrix_correct(size):
    raise AttributeError("Matrix not correct")

while start_point is None or not (0 < start_point <= size):
    point = input(str.format("Введите стартовую вершину маршрута (от 1 до {}): ", size))
    if point.isdigit():
        start_point = int(point)

# отнимаем единицу, так как вводим номера с единицы, а считаем с нуля
result_path = min_path(start_point - 1, size)
print(str.format("Стоимость минимального маршрута: {}", result_path.length))
print(str.format("Минимальный маршрут: {}", result_path.route_str))
input("Нажмите Enter для выхода")