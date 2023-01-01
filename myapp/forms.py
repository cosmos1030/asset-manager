from django import forms
from myapp.models import Stock_post

class StockChangeForm(forms.Form):
    name = forms.CharField(label="Stock Name", max_length=100, error_messages={
        "required": "Your name must not be empty!",
        "max_length": "Please enter a shorter name!"
    })
    amount = forms.IntegerField(label="How many")

class PostForm(forms.ModelForm):
    class Meta:
        model = Stock_post  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        labels = {
            'subject': '제목',
            'content': '내용',
        }