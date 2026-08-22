from django import forms
from django.forms import inlineformset_factory
from .models import Post, Comment, Paragraph
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'tags',
            'excerpt',
            'cover',
            'status',
        ]

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise ValidationError('titre obligatoire')
        return title

    def clean_status(self):
        status = self.cleaned_data['status']
        valid_statuses = dict(Post.STATUS)
        if status not in valid_statuses:
            raise ValidationError('status invalide')
        return status


class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = ['text', 'image', 'order']
        widgets = {
            'title':forms.TextInput(attrs={'class':'border-none'}),
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'textarea textarea-bordered w-full'}),
            'image': forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered file-input-sm w-full'}),
            'order': forms.NumberInput(attrs={'class': 'input input-bordered input-sm w-20'}),
            
        }


ParagraphFormSet = inlineformset_factory(
    Post,
    Paragraph,
    form=ParagraphForm,
    extra=9,  # nombre max de blocs ajoutables dynamiquement côté front
    can_delete=True,
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Écris un commentaire...',
                'class': 'textarea textarea-bordered w-full',
            }),
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text.strip():
            raise ValidationError('le commentaire ne peut pas être vide')
        return text