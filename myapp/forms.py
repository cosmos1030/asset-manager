from django import forms


class StockChangeForm(forms.Form):
    stock_name = forms.CharField(label="Stock Name", max_length=100, error_messages={
        "required": "Your name must not be empty!",
        "max_length": "Please enter a shorter name!"
    })
    change_amount = forms.IntegerField(label="How many?")