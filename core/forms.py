from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':30}), required=False)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)

    class Meta:
        model = Todo
        fields = ['title', 'description', 'date', 'time']