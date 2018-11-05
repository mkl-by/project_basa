from django.shortcuts import render, redirect
from .models import Post, TechPost, DocPost, OpisPost, SerPost
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView, View, TemplateResponseMixin
from django.views.generic.list import ListView
from django.db.models import Count
from .forms import GoodForm, SelectForm, DataForm_doc, SelectForma
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
            viborka = viborka.exclude(doc_name__doc_n=None)
        elif podstanovka[0] == 'tech_name__tech_n':
            viborka = viborka.exclude(tech_name__tech_n=None)
        elif podstanovka[0] == 'opis_name__opis_n':
            viborka = viborka.exclude(opis_name__opis_n=None)

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


# -----------------------------------------удаление данных----------------------------------------------------
class DataDel(TemplateView):
    template_name = 'data_del.html'

    def get(self, request, *args, **kwargs):
        if request.GET:

            print(request.GET['element'])
            sas = SelectForma()
            print('-------------------------------', sas)
            sas.fields['form'].queryset = Post.objects.filter(tech_name__tech_n=request.GET['element'])
            print('-------------------------------')
            return render(request, 'data_del.html', {'formm': request.GET['element']})
        else:
            return super(DataDel, self).get(request, *args, **kwargs)



    def get_context_data(self, **kwargs):
        self.form = SelectForm(
            choices=tuple(set([(x['tech_name__tech_n'], x['tech_name__tech_n']) for x in
                               Post.objects.all().values('tech_name__tech_n')])))

        context = super(DataDel, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context





        # print('aaaaaaaaaaaaaaa', request.POST['element'])
