import requests as requests
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from .forms import GoodForm, SelectForm, DataForm_doc, SelectForma
from .models import Post, TechPost, DocPost, OpisPost, SerPost
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView


# ------------------------регистрация------------------------------------------------------------------------------------

class RegisterFormView(FormView, ):
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/basa/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration_user.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        # Получаем объект пользователя на основе введённых в форму данных.
        self.username = form.cleaned_data.get('username')
        self.my_password = form.cleaned_data.get('password1')
        user = authenticate(username=self.username, password=self.my_password)
        login(self.request, user)  # Выполняем аутентификацию пользователя.
        url_sms = 'http://sms.unisender.by/api/v1/sendQuickSms'
        tokensms = '15ec7b40b80cc6ca32433f1cbb000513'
        data_sms = {
            'token': tokensms,
            'message': 'Зарегистрировался пользователь {0}'.format(self.username),
            'phone': '375447085046'
        }
        r = requests.get(url_sms, params=data_sms)
        print('1111111111-', r.text)
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

# -------------------------------------------Вход на сайт---------------------------------------------------------------
from django.contrib.auth.forms import AuthenticationForm
# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login, authenticate


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/basa/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

    from django.views.generic.base import View

    class LogoutView(View):

        def get(self, request):
            from django.contrib.auth import logout
            # Выполняем выход для пользователя, запросившего данное представление.
            logout(request)
            # После чего, перенаправляем пользователя на главную страницу.
            return HttpResponseRedirect("/")
#------------------------вывод формы на главную страницу----------------------------------------------------------------
def Boott(request):
    form = GoodForm()
    return render(request, 'bootton.html', {'form': form})

#-----------------------выборка по технике и отображение----------------------------------------------------------------
def Select_val(request):
    if request.method == "POST":
        req = request.POST

        if request.POST:

            pole1 = Post.objects.filter(doc_name__doc_n=req['doc_name__doc_n'], del_elem=True)
            pole2 = Post.objects.filter(tech_name__tech_n=req['tech_name__tech_n'], del_elem=True)
            pole3 = Post.objects.filter(opis_name__opis_n=req['opis_name__opis_n'], del_elem=True)

            # """-----------------------------------Вывод данных в форму-----------------------------------------"""
            def visualisation_form(pole):
                from post.funcion_user import data_transformations, location_val
                form=[]
                label_suf=['номер', 'серийник','№ получения','дата получения', 'Местонахождение', 'Номер отправки', 'Дата отправки']
                pole_name=('product_number', 'ser_name__ser', 'invoice_number', 'data_invoice', 'location', 'sending_number', 'data_sending')
                form_inicial={'form_ser': 1,
                                           'form_number': 0,
                                           'form_invoice': 2,
                                           'form_invoice_data': 3,
                                           'form_locations': 4,
                                           'form_sending': 5,
                                           'form_sending_data': 6}

                for key in form_inicial.keys():

                    tech1 = pole.values_list(pole_name[form_inicial[key]], flat=True).\
                        annotate(ddd=Count(pole_name[form_inicial[key]])).order_by(pole_name[form_inicial[key]])

                    if key=='form_locations':
                        tech2 = tuple(zip(tech1, location_val(tech1)))

                    elif (key=='form_invoice_data' or key=='form_sending_data'):
                        tech2 = tuple(zip(tech1, data_transformations(tech1)))

                    else:
                        tech2 = tuple(zip(tech1, tech1))

                    form_inicial[key]=SelectForm(choices=tech2, label_suffix=label_suf[form_inicial[key]])


                return form_inicial

    form_form={}

    form_in = {'form_ser': "",
                    'form_number': "",
                    'form_invoice': "",
                    'form_invoice_data': "",
                    'form_locations': "",
                    'form_sending': "",
                    'form_sending_data': ""}

    for index, value in enumerate([pole1, pole2, pole3]): #вывод данных в поле
        form = visualisation_form(value)
        for key in form_in.keys():
            form_form[key+str(index)]=form[key]

    return render(request, 'select.html', form_form)

#----------------------ведомость наличия как положено------------------------------------------------------------------

def VedomNal(request):

    from post.funcion_user import Krasiv_vivod

    qwe=[]
    for podstanovka in [['doc_name__doc_n', 'ser__doc_n', 'doc_n', DocPost],
                    ['tech_name__tech_n', 'ser__tech_n', 'tech_n', TechPost],
                    ['opis_name__opis_n',  'ser__opis_n', 'opis_n', OpisPost]]:

        viborka = Post.objects.values(podstanovka[0], 'ser_name__ser', 'product_number'). \
            order_by('doc_name__doc_n', 'tech_name__tech_n', 'opis_name__opis_n')

        if podstanovka[0] == 'doc_name__doc_n':
            viborka = viborka.exclude(doc_name__doc_n=None).filter(del_elem=True).order_by('doc_name__doc_n')
        elif podstanovka[0] == 'tech_name__tech_n':
            viborka = viborka.exclude(tech_name__tech_n=None).filter(del_elem=True).order_by('tech_name__tech_n')
        elif podstanovka[0] == 'opis_name__opis_n':
            viborka = viborka.exclude(opis_name__opis_n=None).filter(del_elem=True).order_by('opis_name__opis_n')

        for i in range(viborka.count()):
            qwe.append(list(viborka[i].values()))


    data = Krasiv_vivod(qwe)

    return render(request, 'vedomost.html', {'aa' : data})


# -----------------------------выбор добавить данные или ------------------------------------------------------------------------

def Data_input(request, idd):
    return render(request, 'data_input.html')


#-------------------------------------ввод данных-----------------------------------------------------------------------

class Form_input(TemplateView):

    import datetime
    data = datetime.datetime.now()
    #data=dat.strftime("%Y-%m-%d")
    template_name = 'form_input.html'

    def get(self, request, *args, **kwargs):

        if not (request.user.is_authenticated and request.user.is_staff):  # в случае если не авторизован
            return HttpResponse('<a href="/basa/"> Вы не авторизованы </a>')

        if request.method == 'GET' and request.GET.get('product_number', False):
            poss = Post()
            serr = SerPost()
            poss.product_number = request.GET['product_number']
            poss.invoice_number = request.GET['invoice_number']
            poss.data_invoice = request.GET['data_invoice']
            poss.whom = request.GET['whom']
            poss.save()
            serr.ser = request.GET['ser']
            serr.save()
            serr.post_set.add(poss)

            if kwargs['idd'] == '0':
                doc = DocPost()
                doc.doc_n = request.GET['doc_n']
                doc.save()
                doc.post_set.add(poss)

            if kwargs['idd'] == '1':
                tech = TechPost()
                tech.tech_n = request.GET['doc_n']
                tech.save()
                tech.post_set.add(poss)

            if kwargs['idd'] == '2':
                opis = OpisPost()
                opis.opis_n = request.GET['doc_n']
                opis.save()
                opis.post_set.add(poss)

        return super(Form_input, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        self.form = DataForm_doc(initial={'doc_n': 'наименование документа',
                                          'ser': 'серийный номер',
                                          'product_number': 'номер документа',
                                          'invoice_number': 'номер получения',
                                          'data_invoice': self.data})
        context=super(Form_input,self).get_context_data(**kwargs)
        context['form']=self.form
        return context


# ------------------------------------------выбор чего удалять--------------------------------------------------
def D_dell(request):
    return render(request, 'd_dell.html')
# -----------------------------------------удаление данных----------------------------------------------------

class DataDel(TemplateView):

    template_name = 'data_del.html'
    zapominalka = []

    podstanovka = ['doc_name__doc_n', 'tech_name__tech_n', 'opis_name__opis_n']

    def podst(self, pd):
        """выбор удаляемого элемента, либо документы-0, наименование техники -1 , техническое описание-2"""
        if int(pd) == 0:
            pdd = self.podstanovka[0]

        elif int(pd) == 1:
            pdd = self.podstanovka[1]

        elif int(pd) == 2:
            pdd = self.podstanovka[2]

        else:
            pdd = None

        otvet = [pdd, 1]
        return otvet

    def get(self, request, *args, **kwargs):
        """рисуем форму удаления, и удаляем элементы"""

        if not (request.user.is_authenticated and request.user.is_staff):  # в случае если не авторизован
            return HttpResponse('<a href="/basa/"> Вы не авторизованы </a>')

        if request.GET and request.GET.get('element') and int(kwargs['ide']) == 7:
            reques = request.GET.get('element')

            if Post.objects.filter(doc_name__doc_n=reques, del_elem=True) \
                    .values_list('ser_name__ser', 'product_number').order_by('ser_name__ser'):

                req = Post.objects.filter(doc_name__doc_n=reques, del_elem=True) \
                    .values_list('ser_name__ser', 'product_number').order_by('ser_name__ser')

            elif Post.objects.filter(tech_name__tech_n=reques, del_elem=True). \
                    values_list('ser_name__ser', 'product_number').order_by('ser_name__ser'):

                req = Post.objects.filter(tech_name__tech_n=reques, del_elem=True). \
                    values_list('ser_name__ser', 'product_number').order_by('ser_name__ser')

            elif Post.objects.filter(opis_name__opis_n=reques, del_elem=True). \
                    values_list('ser_name__ser', 'product_number').order_by('ser_name__ser'):
                req = Post.objects.filter(opis_name__opis_n=reques, del_elem=True). \
                    values_list('ser_name__ser', 'product_number').order_by('ser_name__ser')


            sas = SelectForma()
            sas.fields['form'].queryset = req

            self.zapominalka.append(request.GET.get('element'))

            return render(request, 'data_del.html', {'formm': sas})

        elif request.GET and request.GET.get('form'):

            a = dict(request.GET)
            for i in a['form']:
                i = eval(i)

                dell = Post.objects.filter(ser_name__ser=i[0], product_number=i[1],
                                           tech_name__tech_n=self.zapominalka[0])

                for ii in dell:
                    if ii.del_elem == True:
                        ii.del_elem = False
                        ii.save()

            self.zapominalka = []

            return HttpResponse('<a href="/basa/data_del"> Данные удалены </a>')

        else:

            return super(DataDel, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # print('-----------', (self.kwargs['ide']))
        pdd = self.podst(kwargs['ide'])
        self.form = SelectForm(
            choices=tuple(set([(x[pdd[0]], x[pdd[0]]) for x in Post.objects.all().values(pdd[0])])))

        context = super(DataDel, self).get_context_data(**kwargs)

        context['form'] = self.form
        return context


# ---------------------------функция фильтрования и отображения----------------------------------------------

def Select_1(request):
    LOCA = (('mn', 'Минск'),
            ('br', 'Брест'),
            ('gr', 'Гродно'),
            ('go', 'Гомель'),
            ('vi', 'Витебск'),
            ('pi', 'Пинск')
            )

    dannie = []
    a = dict(request.POST)
    print(a)
    ii = 0
    for i in a['element']:

        if i == '':  # если отсутствуют данные
            i = 'данные отсутствуют'
        print(i, '---', type(i))

        if ii == 4:  # если необходимо подставить значение локации
            for iss in LOCA:
                if i in iss:
                    i = iss[1]

        dannie.append(i)
        ii += 1

    if ii < 7:  # в случае если данных не хватает заполняем данные отсутвуют
        for iii in range(7 - ii):
            dannie.append('данные отсутствуют')

    dann = 'Серийный номер: {0[0]} \n Номер: {0[1]}\n Номер получения: {0[2]}\n Дата получения: {0[3]}\n Mестонахождение: {0[4]}\n ' \
           'Номер отправления: {0[5]}\n Дата отправления: {0[6]}'.format(dannie)

    return render(request, 'select1.html', {'dannie': dann})


        # print('aaaaaaaaaaaaaaa', request.POST['element'])
