from django import forms

from common.models import Customer, User, Outorder, Clothes


class OutorderForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    code = forms.CharField(label='入库单号', required=False, max_length=32,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    customer = forms.ModelChoiceField(label='客户', queryset=Customer.objects.all(),
                                      widget=forms.Select({'class': 'form-control'}))
    user = forms.ModelChoiceField(label='经手人', required=False, queryset=User.objects.all(),
                                  widget=forms.Select({'class': 'form-control'}))
    create_time = forms.CharField(label='创建时间', required=False, max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))


class OutorderClothesForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    outorder = forms.ModelChoiceField(label='出库单号', required=False, queryset=Outorder.objects.all(),
                                      widget=forms.Select({'class': 'form-control'}))
    clothes = forms.ModelChoiceField(label='服装', queryset=Clothes.objects.all(),
                                     widget=forms.Select({'class': 'form-control'}))
    amount = forms.IntegerField(label='数量', widget=forms.NumberInput(attrs={'class': 'form-control'}))


class EditmoreForm(forms.Form):
    clothes = forms.ModelChoiceField(label='服装', required=False, queryset=Clothes.objects.all(),
                                     widget=forms.Select({'class': 'form-control', 'disabled': 'disabled'}))
    amount = forms.IntegerField(label='数量', widget=forms.NumberInput(attrs={'class': 'form-control'}))
