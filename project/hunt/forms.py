from django import forms
from hunt.models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), label_suffix='')
    text.label = 'Поделитесь своими мыслями'

    class Meta:
        model = Comment
        fields = ['text']
