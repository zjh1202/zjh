from django import forms
from django.forms import fields, widgets

from word import models


class UserForm(forms.Form):
    job_number = forms.IntegerField(label="学号", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    num = forms.IntegerField(label="做题编号", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # test_number = forms.ChoiceField(label="考试题号：",
    #                                 choices=models.WordAdmin.objects.all().values_list('test_number', 'test_number'))
    #实时化更新
    test_number = fields.IntegerField(label="考试题号：", widget=widgets.Select())

    def __init__(self, *args, **kwargs):
        # 拷贝所有的静态字段，复制给self.fields
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['test_number'].widget.choices = models.WordAdmin.objects.values_list('test_number', 'test_number')


class TeacherUserForm(forms.Form):
    job_number = forms.IntegerField(label="工号", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    num = forms.IntegerField(label="出题编号", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # test_number = forms.ChoiceField(label="考试题号：", choices=models.WordAdmin.objects.all().values_list('test_number','test_number'))
    #实时化更新
    test_number = fields.IntegerField(label="考试题号：", widget=widgets.Select())

    def __init__(self, *args, **kwargs):
        # 拷贝所有的静态字段，复制给self.fields
        super(TeacherUserForm, self).__init__(*args, **kwargs)
        self.fields['test_number'].widget.choices = models.WordAdmin.objects.values_list('test_number', 'test_number')


class RegisterForm(forms.Form):

    job_number = forms.IntegerField(label="学号", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="邮箱", max_length=256, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    school = forms.CharField(label="学校", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    object = forms.CharField(label="科目", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))


class TeacherRegisterForm(forms.Form):

    job_number = forms.IntegerField(label="工号", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="邮箱", max_length=256, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    school = forms.CharField(label="学校", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    object = forms.CharField(label="科目", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))


class TNumber(forms.Form):
    text_number = forms.IntegerField(label='需要创建的题目：', widget=forms.TextInput(attrs={'class': 'form-control'}))


class TeacherForm(forms.Form):
    text = forms.CharField(label='题目',max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    keyword = forms.CharField(label='关键词：', max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text_answer = forms.CharField(label='标准答案：', max_length=256, widget=forms.Textarea(attrs={'class': 'form-control','rows': '3'}))


class TnForm(forms.Form):
    teacher_number = forms.CharField(label='老师的工号：', widget=forms.TextInput(attrs={'class': 'form-control'}))


class StForm(forms.Form):
    answer = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'class': 'form-control'}))


class AdminLogin(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class Submit(forms.Form):
    test_number = forms.IntegerField(label="题号", widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label="科目", widget=forms.TextInput(attrs={'class': 'form-control'}))
    text_number = forms.IntegerField(label='题目数量', widget=forms.TextInput(attrs={'class': 'form-control'}))
