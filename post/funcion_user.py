
#--------------------------------------------трансформация даты---------------------------------------------------------

def data_transformations(data_tr):  # переворачиваем дату
    w = []
    for i in data_tr:
        if i:
            w.append(i.strftime('%d-%m-%Y'))
    return w
#----------------------------------------------значения из локации------------------------------------------------------

def location_val(locations): #достаем значения из локаций
    w = []
    s = Post.LOCATIONS
    for i in locations:
        for ii in range(len(s)):
            if s[ii][0] == i:
                w.append(s[ii][1])
    return w

#---------------------------------------обработка данных ведомости наличия---------------------------------------------
from .models import Post

def Krasiv_vivod(listic):
    """функция принимает список вида listic=[['aa',1,10],['aa',2,11],['aa',4,11],['bb',3,12]]
  и возвращает строки вида '1-2, 4', '3' """

    one = listic[0][0]
    duo = listic[0][1]
    stroka = str(listic[0][2])
    s = [1]

    dddd = ['', ]
    name_n = []
    i = 0

    for index, znach in enumerate(listic[1:]):

        if one == znach[0] and duo == znach[1]:

            ss = abs(int(listic[index][2])) - (int(znach[2]))
            if ss < 0:
                ss = ss * (-1)
            s.append(ss)

            if ss <= 1 and s[-2] == 1:
                dddd.append(listic[index][2])
                dddd.append(znach[2])
                if stroka.count('-') <= 1:
                    stroka = str(dddd[1]) + '-' + str(dddd[-1])
                else:
                    dddd.append(znach[2])
                    stroka = stroka[:(stroka.rfind('-')) + 1] + str(dddd[-1])

            if s[-1] > 1:
                dddd.append(znach[2])
                a = len(dddd) - 1
                stroka = stroka + ', ' + str(dddd[a])

            if s[-2] > 1 and s[-1] == 1:
                dddd.append(znach[2])
                stroka = stroka + '-' + str(dddd[-1])

        elif one != znach[0] or duo != znach[1]:
            if duo==None:
                duo=''
            i = +1
            name_n.append({'id': i, 'name': one, 'serija': duo, 'number': stroka})
            one = znach[0]
            duo = znach[1]
            stroka = str(znach[2])
            s = [1]
            dddd = ['']

    if duo == None:
        duo = ''
    name_n.append({'id': i, 'name': one, 'serija': duo, 'number': stroka})

    return name_n