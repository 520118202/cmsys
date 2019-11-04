from django import forms


class CustomerForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    name = forms.CharField(label='客户名', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='电话', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='地址', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    create_time = forms.CharField(label='创建时间', required=False, max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
