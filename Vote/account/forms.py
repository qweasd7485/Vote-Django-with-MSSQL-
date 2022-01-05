from django import forms
from django.forms import Textarea
from account.models import User
import re

def email_check(email):    
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

class UserForm(forms.ModelForm):      
    username = forms.CharField(label='投票人帳號', max_length=12, required=True)    
    password = forms.CharField(label='投票人密碼', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='信箱', required=True)
    fullName = forms.CharField(label='全名', max_length=10, required=True)
    is_superuser = forms.NullBooleanField(label='是否授予超級使用者權限')
    is_staff = forms.NullBooleanField(label='是否授予後端資料庫管理權限')
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'fullName', 'is_superuser', 'is_staff')