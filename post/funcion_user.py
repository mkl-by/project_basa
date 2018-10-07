def Krasiv_vivod(listic):
    """функция принимает список вида listic=[['aa',1],['aa',2],['aa',4],['bb',3]]
  и возвращает строки вида '1-2, 4', '3' """
    listic = sorted(listic)
    one = listic[0][0]
    stroka = str(listic[0][1])  # задаем начальное значение строки
    s = []  # необходим в случае если два последних значения >=2
    dd = len(listic)
    i=0
    name_n=[]
    for index, znach in enumerate(listic[1:]):
        if one == znach[0]:
            ss = abs(int(listic[index][1]) - int(znach[1]))  # вычисляем разницу между последним и предыдущим значением
            s.append(ss)

            if ss >= 2 and s[-1] >= 2 and s[-2] >= 2:  # если два последних значения с разницей >=2
                stroka = stroka + str(znach[1]) + ','

            elif ss >= 2:  # иначе если значения идут по порядку 4,5,6,7 c шагом 1
                if stroka.endswith(', '):
                    stroka = stroka.rstrip(', ')
                stroka = stroka + '-'
                stroka = stroka + str(listic[index][1]) + ', '
                stroka = stroka + str(znach[1]) + ', '

            elif ss == 1 and dd == index + 2:  # иначе определение последнего элемента с шагом 1
                if stroka.endswith(', '):
                    stroka = stroka.rstrip(', ')
                stroka = stroka + '-'
                stroka = stroka + str(znach[1])


        else:
            stroka = stroka.rstrip(', ')
            #name[one] = stroka  # заносим данные в словарь
            # name['name']=one
            # name['stroka']=stroka
            i+=1
            name_n.append({'id': i,'name':one, 'stroka':stroka}) #создаем словарь вывода элементов
            #print(stroka)
            stroka = str(znach[1])  # инициализируем 1й элемент в строке
            one = znach[0]  # переходим на "аа"

    #print(stroka)
    #name[one] = stroka  # вносим последние значения в словарь
    # name['name'] = one
    # name['stroka'] = stroka
    name_n.append({'id':(i+1),'name':one, 'stroka':stroka}) #создаем базу
    return name_n