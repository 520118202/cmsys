from django import forms


class UserForm(forms.Form):
    role_choices = (
        ('操作员', '操作员'),
        ('管理员', '管理员')
    )
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    username = forms.CharField(label="用户名", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="姓名", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label="角色", choices=role_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    create_time = forms.CharField(label='创建时间', required=False, max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
