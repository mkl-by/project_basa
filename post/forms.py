from django import forms
from .models import Post, DocPost
from django.db.models import Count

class GoodForm(forms.ModelForm):


        #queryset1 = Post.objects.values(fieldss).annotate(dcount=Count(fieldss)).values_list(fieldss, flat=True).order_by(fieldss)
    # values_list('product_number', flat=True).order_by('product_number') достаем кортеж и если флат=тру, возвращаем единственное значение
    # Post.objects.values('product_number').annotate(dcount=Count('product_number')) достаем номера в единственном экземпляре


    doc_name__doc_n=forms.ModelChoiceField( queryset = Post.objects.values('doc_name__doc_n').
                                            annotate(dcount=Count('doc_name__doc_n')).
                                            values_list('doc_name__doc_n', flat=True).
                                            order_by('doc_name__doc_n'), widget=forms.Select, label='Документы')  # создаем поле

    tech_name__tech_n=forms.ModelChoiceField(queryset = Post.objects.values('tech_name__tech_n').
                                            annotate(dcount=Count('tech_name__tech_n')).
                                            values_list('tech_name__tech_n', flat=True).
                                            order_by('tech_name__tech_n'), widget=forms.Select, label='Техника')

    opis_name__opis_n = forms.ModelChoiceField(queryset = Post.objects.values('opis_name__opis_n').
                                            annotate(dcount=Count('opis_name__opis_n')).
                                            values_list('opis_name__opis_n', flat=True).
                                            order_by('opis_name__opis_n'), widget=forms.Select, label='Техническое описание')

    class Meta:
        model=Post
        fields=('doc_name__doc_n', 'tech_name__tech_n', 'opis_name__opis_n' )



class SelectForm(forms.Form):
    """форма получает сет и во вьюшке, переопределен параметр choices"""
    element = forms.ChoiceField(label=" ", required=False)


    def __init__(self, *args, **kwargs):
        choices=kwargs.pop('choices')
        super(SelectForm, self).__init__(*args, **kwargs)
        if choices:
            self.fields['element'].choices=choices





   # self.clean()

