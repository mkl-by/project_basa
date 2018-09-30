from django.shortcuts import render
from .models import Post, TechPost, DocPost, OpisPost, SerPost
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.db.models import Count
from .forms import GoodForm, SelectForm

# class Home(TemplateView):
#    template_name = "home.html"

'''
class Bootton(ListView):
    template_name = 'bootton.html'
    queryset = Post.objects.values('product_number').annotate(dcount=Count('product_number'))
    context_object_name='number_product'
'''


def Boott(request):
    form = GoodForm()

    return render(request, 'bootton.html', {'form': form})


def Select_val(request):
    if request.method == "POST":
        req = request.POST

        if request.POST:
            doc = Post.objects.filter(doc_name__doc_n=req['doc_name__doc_n'], del_elem=True)
            print(doc)
            data = doc.values_list('doc_name__post__product_number', flat=True)

            # """-----------------------------------Выборка по технике-----------------------------------------"""
            tech = Post.objects.filter(tech_name__tech_n=req['tech_name__tech_n'])
            tech1 = tech.values_list('product_number', flat=True).annotate(ddd=Count('product_number'))  # номер
            tech2 = tuple(zip(tech1, tech1))
            form_number = SelectForm(choices=(tech2), label_suffix='техника')

            tech_ser = tech.values_list('ser_name__ser', flat=True).annotate(ddd=Count('ser_name__ser'))  # серийник
            tech_ser = tuple(zip(tech_ser, tech_ser))
            form_ser = SelectForm(choices=tech_ser, label_suffix='серийник')

            invoice_num = tech.values_list('invoice_number', flat=True).annotate(
                ddd=Count('invoice_number'))  # № получения
            invoice_num = tuple(zip(invoice_num, invoice_num))
            form_invoice = SelectForm(choices=invoice_num, label_suffix='№ получения ')

            invoice_data = tech.values_list('data_invoice', flat=True).annotate(
                ddd=Count('data_invoice'))  # дата получения

            w = []
            for i in invoice_data:
                w.append(i.strftime('%d-%m-%Y'))

            invoice_data = tuple(zip(invoice_data, w))
            form_invoice_data = SelectForm(choices=invoice_data, label_suffix='Дата получения ')

            locations = tech.values_list('location', flat=True).annotate(ddd=Count('location'))  # Местонахождение
            w = []
            s = Post.LOCATIONS
            for i in locations:
                for ii in range(len(s)):
                    if s[ii][0] == i:
                        w.append(s[ii][1])

            locat = tuple(zip(locations, w))
            form_locations = SelectForm(choices=locat, label_suffix='Место нахождения ')

    return render(request, 'select.html', {'form_ser': form_ser, 'form_number': form_number,
                                           'form_invoice': form_invoice, 'form_invoice_data': form_invoice_data,
                                           'form_locations': form_locations})


def SS(request):
    pass
    # print('aaaaaaaaaaaaaaa', request.POST['element'])
