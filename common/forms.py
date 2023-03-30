#Django의 forms 모듈을 가져옴
from django import forms
#Django의 인증 시스템에서 제공하는 UserCreationForm을 가져옴
from django.contrib.auth.forms import UserCreationForm
#Django의 인증 시스템에서 제공하는 User 모델을 가져옴
from django.contrib.auth.models import User

#UserCreationForm을 상속받는 UserForm 클래스를 정의
class UserForm(UserCreationForm):
    #이메일 필드를 추가하고 이메일 필드의 이름은 '이메일'로 지정
    email = forms.EmailField(label="이메일")

    #Meta 클래스를 정의합니다
    class Meta:
        #속성을 User로 설정
        model = User 
        #fields의 속성을 ('username','email')로 설정하고 사용자의 username과 email 필드만 사용
        fields = ("username","email")