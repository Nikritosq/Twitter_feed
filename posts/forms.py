from django import forms

from .models import Post

MAX_LENGTH = 244

class PostFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_LENGTH:
            raise forms.ValidationError("This Post is too long")
        return content