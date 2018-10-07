from django.shortcuts import render
from .models import Post, TechPost, DocPost, OpisPost, SerPost
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.db.models import Count
from .forms import GoodForm, SelectForm

def Boott(request):
    form = GoodForm()
    return render(request, 'bootton.html', {'form': form})

#-----------------------выборка по технике и отображение-------------------------------------------------------
def Select_val(request):
    if request.method == "POST":
        req = request.POST

        if request.POST:

            pole1 = Post.objects.filter(doc_name__doc_n=req['doc_name__doc_n'], del_elem=True)
            pole2 = Post.objects.filter(tech_name__tech_n=req['tech_name__tech_n'], del_elem=True)
            pole3 = Post.objects.filter(opis_name__opis_n=req['opis_name__opis_n'], del_elem=True)

            # """-----------------------------------Вывод данных в форму-----------------------------------------"""
            def visualisation_form(pole):

                def data_transformations(data_tr):  # переворачиваем дату
                    w = []
                    for i in data_tr:
                        if i:
                            w.append(i.strftime('%d-%m-%Y'))
                    return w

                def location_val(locations): #достаем значения из локаций
                    w = []
                    s = Post.LOCATIONS
                    for i in locations:
                        for ii in range(len(s)):
                            if s[ii][0] == i:
                                w.append(s[ii][1])
                    return w

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
    qqq=[]
    for i_tech in TechPost.objects.select_related('tech_n__tech_name').values():
        for i_ser in SerPost.objects.select_related('ser__tech_n').values():
            queri=Post.objects.filter(tech_name__tech_n=i_tech['tech_n'], ser_name_id=i_ser['id'])
            if queri.count()==0:
                continue
            qqq.append([i_tech['tech_n'], i_ser['ser']])

    print(Krasiv_vivod(qqq))
    data=Krasiv_vivod(qqq)
    # s=Vedomosti()
    # s.get_context_data(Krasiv_vivod(qqq))

    return render(request, 'vedomost.html', {'aa' : data})


            #qww[i_tech['tech_n']]  =  i_ser['ser']
            #qqq.append(i_ser['ser'])


            # if i_tech['tech_n'] in qww.keys():
            #     qww[(i_tech['tech_n'])]=qqq
            # else:
            #     qqq = []
            #     qww[(i_tech['tech_n'])] =

                    #qww[i_tech['tech_n']] = qqq.append((i_ser['ser']))


#----------------------ведомость наличия--------------------------------------------------------------------------------
# class Vedomosti(TemplateView):
#     model = Post
#     template_name = 'vedomost.html'
#     paginate_by = 30
#     #a = Post.objects.all().filter(del_elem=True).annotate(ddd=Count('product_number')).order_by()
#     #print('------------------->', VedomNal())
#     def get_context_data(self, **kwargs):
#         context = ({
#            'a' : self.kwargs,
#         })
#         return context







def SS(request):
    pass
    # print('aaaaaaaaaaaaaaa', request.POST['element'])
