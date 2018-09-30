from django.db import models
from django.contrib import admin

class Post(models.Model):
    """таблица хранящая данные прихода и отправки в города"""
    LOCATIONS=(('mn','Минск'),
               ('br','Брест'),
               ('gr','Гродно'),
               ('go','Гомель'),
               ('vi','Витебск'),
               ('pi','Пинск')
               )
    WHOM=(('p', 'Питер'),
          ('m','Москва'),
          ('k','Краснодар')
          )
    NAME_FIELD=['doc_name', 'tech_name', 'opis_name','ser_name',
                'product_number', 'invoice_number', 'data_invoice', 'sending_number'
                ]
    del_elem=models.BooleanField(default='True', verbose_name='on/off')
    product_number=models.CharField(max_length=30, blank=True, null=True, verbose_name='number')
    invoice_number=models.CharField(max_length=30, verbose_name='invoice',blank=True, null=True)
    data_invoice=models.DateField(blank=True, null=True)
    sending_number=models.CharField(max_length=30, verbose_name='sending', blank=True, null=True)
    data_sending=models.DateField(blank=True, null=True)
    whom=models.CharField(max_length=30, choices=WHOM, blank=True, null=True)
    location=models.CharField(  max_length=2, choices=LOCATIONS, blank=True, null=True)
    opis_name = models.ForeignKey('OpisPost', on_delete=models.CASCADE, blank=True, null=True)
    doc_name = models.ForeignKey('DocPost', on_delete=models.CASCADE, blank=True, null=True)
    tech_name = models.ForeignKey('TechPost', on_delete=models.CASCADE, blank=True, null=True)
    ser_name=models.ForeignKey('SerPost', on_delete=models.CASCADE,  blank=True, null=True)

    class Meta:
        ordering=['data_invoice']
        def __init__(self):
            return ('%d-%m-%Y'.format(self.data_invoice))


class DocPost(models.Model):
    """Таблица наименования документа, привязана к основной таблице"""
    doc_n=models.CharField(max_length=20)
    class Meta:
        ordering=['doc_n']

    def __str__(self):
        return self.doc_n

class TechPost(models.Model):
    """Таблица наименования техники, привязана к основной таблице"""
    tech_n=models.CharField(max_length=80)

    class Meta:
        ordering=['tech_n'] #сортировка

    def __str__(self):
        return self.tech_n

class OpisPost(models.Model):
    """Таблица наименования тех. описания, привязана к основной таблице"""
    opis_n = models.CharField(max_length=80)

    class Meta:
        ordering=['opis_n'] #сортировка

    def __str__(self):
        return self.opis_n

class SerPost(models.Model):
    """Таблица количества элементов, привязана к основной таблице"""

    ser=models.CharField(max_length=10)

    class Meta:
        ordering=['ser']

    def __str__(self):
        return self.ser

class AdminPost(admin.ModelAdmin):

    list_display = ['doc_name',
                    'tech_name',
                    'opis_name',
                    'ser_name',
                    'product_number',
                    'invoice_number',
                    'data_invoice',
                    'location',
                    'del_elem',
                    'data_sending',
                    ]

