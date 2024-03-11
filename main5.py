import numpy as np

# Здесь твои значения a1, a2, a3, a4, a5
a1, a2, a3, a4, a5 = 1, 2, 3, 4, 5

# Задаем целевую функцию и ограничения
objective = [a1, a2, a3, a4, a5]
constraints = [
    [2, 1, 3, 2, 1, 10],
    [1, 3, 2, 1, 2, 8],
    [3, 2, 3, 3, 3, 15],
    [1, 2, 0, 1, 0, 5],  # Неравенство 
    [0, 0, 2, 0, 3, 1],  # Неравенство 
    [0, 1, 1, 0, 2, 3]   # Неравенство
]

# Количество дополнительных переменных
num_slack = 1   # Для '<=' неравенства
num_surplus = 2 # Для '>=' неравенств

# Приводим задачу к каноническому виду
for i, constraint in enumerate(constraints):
    # Добавляем slack переменные для '<=' неравенства
    if i == 4:  # Индекс строки с '<=' неравенством
        constraint.insert(-1, 1)
        constraints[4] = constraint + [0] * num_surplus
    # Добавляем переменные для '>=' неравенств
    elif i in [3, 5]:
        constraint.insert(-1, -1)
        constraint += [1] + [0] * (num_surplus - (i - 3)) 

# Добавить переменные в целевую функцию с противоположным знаком
for i in range(num_surplus):
    objective.append(0)  # Коэффициенты для переменных
objective += [-1] * num_surplus  # Коэффициенты для переменных

# Создаем симплекс-таблицу
simplex_table = np.array(constraints + [objective + [0]])

# Выводим исходную задачу
print("Исходная задача:")
print(f"F(x) = {' + '.join([f'{coef}x{i+1}' for i, coef in enumerate(objective[:-num_surplus])])}")
for constraint in constraints[:-num_surplus]:
    print(f"{' + '.join([f'{coef}x{i+1}' for i, coef in enumerate(constraint[:-1])])} = {constraint[-1]}")

# Выводим канонический вид
print("\n Канонический вид:")
for constraint in simplex_table[:-1]:
    print(f"{' + '.join([f'{coef}x{i+1}' for i, coef in enumerate(constraint[:-1])])} + s = {constraint[-1]}")

# Выводим симплекс-таблицу с подписями
print("\n Симплекс-таблица:")
labels = [f"x{i+1}" for i in range(len(objective)-num_surplus)] + [f"s{i+1}" for i in range(num_slack)] + [f"s'{i+1}" for i in range(num_surplus)] + ["Solution"]
print("    " + "\t".join(labels))
for row in simplex_table:
    print("\t".join([f"{num:5.2f}" for num in row]))

def simplex_algorithm(table, num_vars, num_constraints):
    num_total_vars = num_vars + num_constraints + num_constraints
    while any(value < 0 for value in table[-1][:-1]): 
        # Выбираем разрешающий столбец (по правилу Бленда, берем первый отрицательный коэффициент)
        pivot_col = next(index for index, value in enumerate(table[-1][:-1]) if value < 0)
        pivot_col -= 2
        # Если все элементы в столбце <= 0, решения нет (задача неограничена)
        if all(row[pivot_col] <= 0 for row in table[:-1]):
            raise ValueError("The problem is unbounded.")
        
        # Разрешающая строка по минимальному отношению элемента столбца решений к элементу разрешающего столбца
        ratios = [row[-1] / row[pivot_col] if row[pivot_col] > 0 else float('inf') for row in table[:-1]]
        pivot_row = ratios.index(min(ratios))
        
        # Делаем разрешающий элемент равным 1 и обнуляем столбец разрешающего элемента
        pivot_element = table[pivot_row][pivot_col]
        table[pivot_row] = [value / pivot_element for value in table[pivot_row]]
        
        for i in range(len(table)):
            if i != pivot_row:
                factor = table[i][pivot_col]
                table[i] = [table[i][j] - factor * table[pivot_row][j] for j in range(len(table[pivot_row])-4)]
    
    # Извлечение решения
    solution = [0] * num_total_vars
    for i in range(num_constraints):
        solution[i] = table[i][-1]
    
    # Обрезаем переменную решения до интересующих нас переменных
    return solution[:num_vars]

# Теперь вызываем алгоритм на нашей симплекс-таблице
final_solution = simplex_algorithm(simplex_table, len(objective) - num_surplus - num_slack, len(constraints))

print(f"Решение: {final_solution}")