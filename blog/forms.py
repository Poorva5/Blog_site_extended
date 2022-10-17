from .models import Comment, Post
from django import forms  #django has two base classes to build form 1. Form and 2. ModelForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('category','title','image' ,'body', 'status',  'tags')
    
    def __int__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in ( self.fields['image'], self.fields['title'], self.fields['body'], self.fields['status'], self.fields['tags']):
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
    


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'body']

        def save(self, commit=False):
            posts = self.instance
            posts.title = self.cleaned_data['title']
            posts.body = self.cleaned_data['body']

            if self.cleaned_data['image']:
                posts.image = self.cleaned_data['image']
            if commit:
                posts.save()
            return posts

        def __init__(self, *args, **kwargs):
            super(UpdatePostForm, self).__init__(*args, **kwargs)
            for field in (self.fields['title'], self.fields['body']):
                field.widget.attrs.update({'class': 'form-control'})
            self.fields['image'].widget.attrs.update({'class': 'form-control-file'})




    


            
