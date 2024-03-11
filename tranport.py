def printTable(A, B, C):
    print("\t", end='')  # Добавляем отступ перед выводом значений столбцов
    for b in B:
        print(b, "\t", end='')  # Выводим подписи столбцов с отступом
    print()
    
    for i in range(len(A)):
        print(A[i], "\t", end='')  # Выводим подписи строк с отступом
        for j in range(len(B)):
            print(C[i][j], "\t", end='')  # Выводим значения из таблицы с отступом
        print()

def doClosedView(A, B, C):
    print("-----------------------------------")
    print("Входные данные")
    printTable(A, B, C)
    print()
    if (sum(A) == sum(B)): # проверям на закрытость (Суммы потребностей и запасов равны)
        print("Задача уже закрытая.")
    else:
        print("Задача не закрытая")
        if (sum(A) > sum(B)):
            print("Добавляем мнимого потребителя")
            B.append(abs(sum(A) - sum(B)))
            for row in C:  
                row.extend([0])
            printTable(A, B, C)
        else:
            print("Добавляем мнимого поставщика")
            A.append(abs(sum(A) - sum(B)))
            C.append([0]*len(B))
            printTable(A, B, C)