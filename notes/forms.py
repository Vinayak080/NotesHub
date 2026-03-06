from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    tags = forms.CharField(
        help_text="Enter tags separated by commas",
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'subject', 'description', 'file', 'tags']
