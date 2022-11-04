from django import forms

class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': '5', 'class' : 'form-control mb-3'}), max_length=160)